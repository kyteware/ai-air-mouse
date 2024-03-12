use std::{f32::consts::PI, fs::File, io::{BufReader, Read}, process::exit, time::Instant};
use byteorder::{LittleEndian, ByteOrder};
use nalgebra::Vector3;
use ahrs::{Ahrs, Madgwick};

const NEW_PACKET_MAGIC: [u8; 11] = *b"stupidglove";
const ERROR_MAGIC: [u8; 11] = *b"glovebroken";

#[derive(Debug)]
struct Packet {
    acc: Vector3<f32>,
    gyr: Vector3<f32>,
    mag: Vector3<f32>
}

impl Packet {
    fn parse(raw: &[u8; 36]) -> Self {
        Self {
            acc: Vector3::new(LittleEndian::read_f32(&raw[0..4]), LittleEndian::read_f32(&raw[4..8]), LittleEndian::read_f32(&raw[8..12])),
            gyr: Vector3::new(LittleEndian::read_f32(&raw[12..16]), LittleEndian::read_f32(&raw[16..20]), LittleEndian::read_f32(&raw[20..24])),
            mag: Vector3::new(LittleEndian::read_f32(&raw[24..28]), LittleEndian::read_f32(&raw[28..32]), LittleEndian::read_f32(&raw[32..36]))
        }
    }
}

fn main() {
    let mut dev = BufReader::new(File::open("/dev/cu.usbmodem14501").unwrap());
    let mut magic_buf = [0u8; 11];

    dev.read_exact(&mut magic_buf).unwrap();
    if magic_buf == ERROR_MAGIC {
        println!("device error");
        exit(1);
    }

    if magic_buf != NEW_PACKET_MAGIC {
        let mut found = false;
        for _ in 0..35 {
            magic_buf.rotate_left(1);
            dev.read_exact(&mut magic_buf[10..11]).unwrap();
            if magic_buf == NEW_PACKET_MAGIC {
                found = true;
                break;
            }
        }
        if !found {
            println!("not a glove");
            exit(1);
        }
    }

    let mut filter = Madgwick::new(0.0012, 0.1);
    
    let mut first_packet = true;
    let mut packet_buf = [0; 36];
    loop {
        if first_packet {
            first_packet = false;
        } else {
            dev.read_exact(&mut magic_buf).unwrap();
            if magic_buf != NEW_PACKET_MAGIC {
                println!("device error");
                exit(1);
            }
        }
        
        dev.read_exact(&mut packet_buf).unwrap();
        let packet = Packet::parse(&packet_buf);

        let orientation = filter.update(
            &(packet.gyr * (PI / 180.0)),
            &(packet.acc / 1000.),
            &(packet.mag / 1000.)
        ).unwrap().euler_angles();

        println!("pitch: {:+06.3} roll: {:+06.3} yaw: {:+06.3}", orientation.0 * 180. / PI, orientation.1 * 180. / PI, orientation.2 * 180. / PI);
    }
}
