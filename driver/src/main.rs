use std::{fs::File, io::Read};

fn main() {
    let mut dev = File::open("/dev/cu.usbmodem14501").unwrap();
    loop {
        let mut res = [0; 1];
        dev.read(&mut res).unwrap();
        print!("{}", res[0] as char);
    }
}
