use std::{fs::File, io::{BufReader, Read}, process::exit, time::Instant};
use byteorder::{LittleEndian, ByteOrder};
use nalgebra::Vector3;

#[derive(Debug)]
struct Packet {
    acc: Vector3<f32>,
    gyr: Vector3<f32>
}

impl Packet {
    fn parse(raw: &[u8; 24]) -> Self {
        Self {
            acc: Vector3::new(LittleEndian::read_f32(&raw[0..4]), LittleEndian::read_f32(&raw[4..8]), LittleEndian::read_f32(&raw[8..12])),
            gyr: Vector3::new(LittleEndian::read_f32(&raw[12..16]), LittleEndian::read_f32(&raw[16..20]), LittleEndian::read_f32(&raw[20..24]))
        }
    }
}

fn main() {
    let mut dev = BufReader::new(File::open("/dev/cu.usbmodem14501").unwrap());
    let mut magic_buf = [0u8; 5];
    dev.read_exact(&mut magic_buf).unwrap();
    if magic_buf != "glove".as_bytes() {
        println!("this isn't a glove");
        exit(1);
    }

    let mut orientation = Vector3::new(0.0, 0.0, 0.0);
    
    let mut err_buf = [0; 1];
    let mut packet_buf = [0; 24];
    let mut last_check: Option<Instant> = None;
    println!("orientation x, orientation y, orientation z, accel x, accel y, accel z");
    for _ in 0..10000 {
        dev.read_exact(&mut err_buf).unwrap();
        if err_buf[0] != 43 {
            println!("device error");
            exit(1);
        }
        dev.read_exact(&mut packet_buf).unwrap();
        let packet = Packet::parse(&packet_buf);

        if let Some(last_check) = last_check {
            let elapsed = last_check.elapsed();

            orientation += packet.gyr * elapsed.as_secs_f32();
        }

        last_check = Some(Instant::now());

        println!("{}, {}, {}, {}, {}, {}", orientation.x, orientation.y, orientation.z, packet.acc.x, packet.acc.y, packet.acc.z);
    }
}
