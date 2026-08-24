// Structural and Behavioral Design Patterns in Rust

use std::sync::Arc;
use tokio::sync::broadcast;

// 1. Adapter Pattern
pub struct LegacyPacket {
    pub raw_bytes: Vec<u8>,
}

pub struct ModernPacket {
    pub payload: String,
    pub length: usize,
}

impl From<LegacyPacket> for ModernPacket {
    fn from(legacy: LegacyPacket) -> Self {
        let payload = String::from_utf8_lossy(&legacy.raw_bytes).to_string();
        let length = payload.len();
        ModernPacket { payload, length }
    }
}

// 2. Strategy Pattern
pub trait CompressionStrategy {
    fn compress(&self, data: &[u8]) -> Vec<u8>;
}

pub struct GzipStrategy;
impl CompressionStrategy for GzipStrategy {
    fn compress(&self, data: &[u8]) -> Vec<u8> {
        let mut out = data.to_vec();
        out.insert(0, 0x1F); // gzip magic byte
        out
    }
}

pub struct ZstdStrategy;
impl CompressionStrategy for ZstdStrategy {
    fn compress(&self, data: &[u8]) -> Vec<u8> {
        let mut out = data.to_vec();
        out.insert(0, 0x28); // zstd magic byte
        out
    }
}

// 3. Observer Pattern
pub struct EventHub {
    pub sender: broadcast::Sender<String>,
}

impl EventHub {
    pub fn new() -> Self {
        let (sender, _) = broadcast::channel(128);
        Self { sender }
    }

    pub fn subscribe(&self) -> broadcast::Receiver<String> {
        self.sender.subscribe()
    }

    pub fn publish(&self, event: String) {
        let _ = self.sender.send(event);
    }
}

// 4. Command Pattern
pub enum AppCommand {
    CreateUser { id: u64, name: String },
    DeleteUser(u64),
    SendEmail { recipient: String, subject: String },
}

impl AppCommand {
    pub fn execute(&self) {
        match self {
            AppCommand::CreateUser { id, name } => println!("Creating user {} with id {}", name, id),
            AppCommand::DeleteUser(id) => println!("Deleting user {}", id),
            AppCommand::SendEmail { recipient, subject } => println!("Sending email to {} with subject {}", recipient, subject),
        }
    }
}

// 5. Template Method Pattern
pub trait DataPipeline {
    fn extract_data(&self) -> Vec<u8>;
    fn transform_data(&self, raw: Vec<u8>) -> String;

    fn run(&self) -> String {
        let raw = self.extract_data();
        self.transform_data(raw)
    }
}

// 6. Composite Pattern
pub enum AstExpr {
    Number(f64),
    Variable(String),
    BinaryOp {
        op: char,
        left: Box<AstExpr>,
        right: Box<AstExpr>,
    },
}

// 7. Iterator Pattern
pub struct RangeStep {
    current: i32,
    stop: i32,
    step: i32,
}

impl Iterator for RangeStep {
    type Item = i32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current < self.stop {
            let res = self.current;
            self.current += self.step;
            Some(res)
        } else {
            None
        }
    }
}
