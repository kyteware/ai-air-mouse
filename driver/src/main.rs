use std::{fs::File, io::{BufReader, Read}, process::exit, time::Instant};
use byteorder::{LittleEndian, ByteOrder};

#[derive(Debug)]
struct Vec3 {
    x: f32,
    y: f32,
    z: f32
}

#[derive(Debug)]
struct Packet {
    acc: Vec3,
    gyr: Vec3
}

impl Packet {
    fn parse(raw: &[u8; 24]) -> Self {
        Self {
            acc: Vec3 { x: LittleEndian::read_f32(&raw[0..4]), y: LittleEndian::read_f32(&raw[4..8]), z: LittleEndian::read_f32(&raw[8..12]) },
            gyr: Vec3 { x: LittleEndian::read_f32(&raw[12..16]), y: LittleEndian::read_f32(&raw[16..20]), z: LittleEndian::read_f32(&raw[20..24]) }
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
    
    let mut err_buf = [0; 1];
    let mut packet_buf = [0; 24];
    let mut last_check: Option<Instant> = None;
    loop {
        dev.read_exact(&mut err_buf).unwrap();
        if err_buf[0] != 43 {
            println!("device error");
            exit(1);
        }
        dev.read_exact(&mut packet_buf).unwrap();
        let packet = Packet::parse(&packet_buf);

        if let Some(last) = last_check {
            let elapsed = last.elapsed();
            if elapsed.as_millis() > 1000 {
                println!("acc: {:?}, gyr: {:?}", packet.acc, packet.gyr);
                last_check = Some(Instant::now());
            }
        } else {
            last_check = Some(Instant::now());
        }
    }
}
