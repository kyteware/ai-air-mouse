use std::{f32::consts::PI, fs::File, io::{BufReader, Read}, process::exit, time::Instant};
use byteorder::{LittleEndian, ByteOrder};
use nalgebra::Vector3;

const NEW_PACKET_MAGIC: [u8; 11] = *b"stupidglove";
const ERROR_MAGIC: [u8; 11] = *b"glovebroken";

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

    let mut orientation = Vector3::new(0.0, 0.0, 0.0);
    
    let mut first_packet = true;
    let mut packet_buf = [0; 24];
    let mut last_check: Option<Instant> = None;
    println!("time, rot x, rot y, rot z, accel x, accel y, accel z");
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

        if let Some(last_check) = last_check {
            let elapsed = last_check.elapsed();

            let adjusted_orientation = orientation + packet.gyr * elapsed.as_secs_f32();
            let gravity_orientation = Vector3::new(roll_from_accel(packet.acc), pitch_from_accel(packet.acc), adjusted_orientation.z);
            orientation = adjusted_orientation * 0.98 + gravity_orientation * 0.02;
        }

        last_check = Some(Instant::now());

        // println!("roll: {:+06.3}, pitch: {:+03.3}, yaw: {:+03.3}", orientation.x, orientation.y, orientation.z);
    }
}

fn pitch_from_accel(acc: Vector3<f32>) -> f32 {
    180. * acc.z.atan2(acc.x) / PI
}

fn roll_from_accel(acc: Vector3<f32>) -> f32 {
    180. * acc.z.atan2(acc.y) / PI
}
