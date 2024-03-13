use driver::Glove;

fn main() {
    let mut glove = Glove::watch("/dev/cu.usbmodem14501");
    loop {
        println!("{:?}", glove.orientation());
        std::thread::sleep(std::time::Duration::from_millis(100));
    }
}
