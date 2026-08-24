// Rust Engineering Principles & Safety Guard Demo

pub trait PaymentProcessor {
    fn process_payment(&self, amount: f64) -> bool;
    fn refund_payment(&self, tx_id: &str) -> bool;
}

// 1. LSP Violation (unimplemented! in trait impl)
pub struct CashPaymentProcessor;

impl PaymentProcessor for CashPaymentProcessor {
    fn process_payment(&self, amount: f64) -> bool {
        println!("Processing cash payment of ${}", amount);
        true
    }

    fn refund_payment(&self, _tx_id: &str) -> bool {
        unimplemented!("Cash payments cannot be refunded electronically");
    }
}

// 2. God Struct (SRP Violation)
pub struct MonolithicManager {
    pub id: u64,
    pub name: String,
    pub db_host: String,
    pub db_user: String,
    pub db_pass: String,
    pub cache_ttl: u32,
    pub log_level: String,
    pub email_host: String,
    pub email_port: u16,
    pub sms_api_key: String,
    pub stripe_key: String,
    pub analytics_id: String,
    pub auth_token: String,
    pub session_timeout: u64,
}

impl MonolithicManager {
    pub fn connect_db(&self) {}
    pub fn disconnect_db(&self) {}
    pub fn query_users(&self) {}
    pub fn update_user(&self) {}
    pub fn send_email(&self) {}
    pub fn send_sms(&self) {}
    pub fn charge_credit_card(&self) {}
    pub fn generate_invoice(&self) {}
    pub fn log_access(&self) {}
    pub fn rotate_keys(&self) {}
    pub fn flush_cache(&self) {}
    pub fn track_pageview(&self) {}
    pub fn parse_webhook(&self) {}
    pub fn backup_database(&self) {}
    pub fn export_metrics(&self) {}
    pub fn render_template(&self) {}
}

// 3. KISS Violation (High Cyclomatic Complexity & Long Parameter List)
pub fn calculate_complex_risk(
    user_id: u64,
    score: f64,
    history_years: u32,
    debt_ratio: f64,
    has_collateral: bool,
    region_code: &str,
) -> f64 {
    let mut risk = 0.0;
    if score > 750.0 {
        risk -= 20.0;
    } else if score > 600.0 {
        risk -= 10.0;
    } else if score > 500.0 {
        risk += 15.0;
    } else {
        risk += 50.0;
    }

    if debt_ratio > 0.5 {
        risk += 25.0;
        if !has_collateral {
            risk += 30.0;
        }
    } else if debt_ratio > 0.3 {
        risk += 10.0;
    }

    if history_years < 2 {
        risk += 15.0;
    } else if history_years > 10 {
        risk -= 10.0;
    }

    if region_code == "HIGH_RISK" {
        risk += 40.0;
    }

    risk
}

// 4. Unsafe Block Guard
pub fn read_memory_raw(ptr: *const u8) -> u8 {
    unsafe {
        *ptr
    }
}
