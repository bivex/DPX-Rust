// Creational Patterns and Idiomatic Rust Patterns

use std::marker::PhantomData;
use std::sync::OnceLock;

// 1. Newtype Pattern
pub struct UserId(pub u64);
pub struct Kilometers(pub f64);

// 2. Builder Pattern
#[derive(Debug)]
pub struct Server {
    pub host: String,
    pub port: u16,
    pub max_connections: usize,
}

pub struct ServerBuilder {
    host: Option<String>,
    port: Option<u16>,
    max_connections: usize,
}

impl ServerBuilder {
    pub fn new() -> Self {
        Self {
            host: None,
            port: None,
            max_connections: 100,
        }
    }

    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    pub fn max_connections(mut self, max: usize) -> Self {
        self.max_connections = max;
        self
    }

    pub fn build(self) -> Result<Server, &'static str> {
        let host = self.host.ok_or("Host is required")?;
        let port = self.port.unwrap_or(8080);
        Ok(Server {
            host,
            port,
            max_connections: self.max_connections,
        })
    }
}

// 3. Factory Method
pub struct Connection {
    pub addr: String,
    pub timeout_ms: u64,
}

impl Connection {
    pub fn new(addr: &str) -> Self {
        Self {
            addr: addr.to_string(),
            timeout_ms: 5000,
        }
    }

    pub fn from_config(addr: &str, timeout_ms: u64) -> Result<Self, &'static str> {
        if addr.is_empty() {
            return Err("Address cannot be empty");
        }
        Ok(Self {
            addr: addr.to_string(),
            timeout_ms,
        })
    }
}

// 4. Typestate Pattern (Compile-time State Machine)
pub struct Unsent;
pub struct Sent;

pub struct HttpRequest<State> {
    pub url: String,
    pub body: Vec<u8>,
    _state: PhantomData<State>,
}

impl HttpRequest<Unsent> {
    pub fn new(url: &str) -> Self {
        Self {
            url: url.to_string(),
            body: Vec::new(),
            _state: PhantomData,
        }
    }

    pub fn send(self) -> HttpRequest<Sent> {
        println!("Sending request to {}", self.url);
        HttpRequest {
            url: self.url,
            body: self.body,
            _state: PhantomData,
        }
    }
}

// 5. RAII / Drop Guard
pub struct FileLockGuard<'a> {
    pub lock_path: &'a str,
}

impl<'a> Drop for FileLockGuard<'a> {
    fn drop(&mut self) {
        println!("Releasing file lock at: {}", self.lock_path);
    }
}

// 6. Singleton Pattern
pub struct GlobalRegistry {
    pub name: String,
}

static REGISTRY: OnceLock<GlobalRegistry> = OnceLock::new();

pub fn get_registry() -> &'static GlobalRegistry {
    REGISTRY.get_or_init(|| GlobalRegistry {
        name: "DefaultRegistry".to_string(),
    })
}
