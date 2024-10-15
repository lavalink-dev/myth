CREATE TABLE IF NOT EXISTS welcome_settings (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT,
    message TEXT
);
CREATE TABLE IF NOT EXISTS goodbye_settings (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT,
    message TEXT
);
CREATE TABLE IF NOT EXISTS boost_settings (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT,
    message TEXT
);
CREATE TABLE IF NOT EXISTS autorole_settings (
    guild_id BIGINT PRIMARY KEY,
    role_id BIGINT
);
CREATE TABLE IF NOT EXISTS vanity_settings (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT
);
CREATE TABLE IF NOT EXISTS username_settings (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT
);
CREATE TABLE IF NOT EXISTS skullboard_settings (
    guild_id BIGINT PRIMARY KEY,
    emoji TEXT DEFAULT '💀',
    channel_id BIGINT,
    reaction_count INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS pingonjoin_settings (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT
);
CREATE TABLE IF NOT EXISTS autorespond_settings (
    guild_id BIGINT PRIMARY KEY,
    trigger TEXT,
    response TEXT
);
CREATE TABLE IF NOT EXISTS autoreact_settings (
    guild_id BIGINT PRIMARY KEY,
    trigger TEXT,
    emoji TEXT
);
CREATE TABLE IF NOT EXISTS invoke_settings (
    guild_id BIGINT PRIMARY KEY,
    command TEXT,
    message TEXT,
    UNIQUE (guild_id, command)
);
CREATE TABLE IF NOT EXISTS joindm_settings (
    guild_id BIGINT PRIMARY KEY,
    message TEXT
);
CREATE TABLE IF NOT EXISTS reactionroles_settings (
    guild_id BIGINT PRIMARY KEY,
    message_id BIGINT,
    emoji TEXT,
    role_id BIGINT
);


CREATE TABLE IF NOT EXISTS prefixes (
    user_id TEXT PRIMARY KEY,
    prefix TEXT
);
CREATE TABLE IF NOT EXISTS blacklist (
    user_id TEXT PRIMARY KEY,
    reason TEXT
);
CREATE TABLE IF NOT EXISTS errors (
    error_id TEXT PRIMARY KEY,
    error_message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS vanityroles (
    guild_id BIGINT PRIMARY KEY,  
    enabled BOOLEAN DEFAULT FALSE, 
    text VARCHAR(255)              
);
CREATE TABLE IF NOT EXISTS vanityroles_roles (
    guild_id BIGINT,            
    role_id BIGINT,              
    PRIMARY KEY (guild_id, role_id), 
    FOREIGN KEY (guild_id) REFERENCES vanityroles(guild_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS voicemaster (
    guild_id BIGINT PRIMARY KEY,         
    category_id BIGINT,                   
    interface_id BIGINT,                  
    create_channel_id BIGINT                 
);
CREATE TABLE IF NOT EXISTS vc_owners (
    channel_id BIGINT PRIMARY KEY,          
    owner_id BIGINT                         
);
CREATE TABLE IF NOT EXISTS automod (
    guild_id BIGINT NOT NULL,
    word TEXT NOT NULL,
    PRIMARY KEY (guild_id, word)
);
CREATE TABLE IF NOT EXISTS antilink (
    guild_id BIGINT NOT NULL,
    pattern TEXT NOT NULL,
    PRIMARY KEY (guild_id, pattern)
);
CREATE TABLE IF NOT EXISTS economy (
    user_id BIGINT PRIMARY KEY,
    balance BIGINT DEFAULT 0
);
CREATE TABLE IF NOT EXISTS streaks (
    user_id BIGINT,
    type TEXT,
    last_claimed TIMESTAMP,
    streak INTEGER DEFAULT 0,
    PRIMARY KEY (user_id, type)
);
