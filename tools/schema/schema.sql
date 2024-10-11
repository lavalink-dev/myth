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
CREATE TABLE IF NOT EXISTS antinuke_settings (
    guild_id BIGINT PRIMARY KEY,
    createchannels BOOLEAN DEFAULT FALSE,
    deletechannels BOOLEAN DEFAULT FALSE,
    roleedit BOOLEAN DEFAULT FALSE,
    roledelete BOOLEAN DEFAULT FALSE,
    rolecreate BOOLEAN DEFAULT FALSE,
    roleadd BOOLEAN DEFAULT FALSE,
    roleremove BOOLEAN DEFAULT FALSE,
    botadd BOOLEAN DEFAULT FALSE,
    punishment VARCHAR(50) DEFAULT 'kick',
    antinuke_enabled BOOLEAN DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS antinuke_logs (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT,
    user_id BIGINT,
    action VARCHAR(50),
    action_count INT DEFAULT 1,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guild_id) REFERENCES antinuke_settings (guild_id)
);
CREATE TABLE IF NOT EXISTS antinuke_admins (
    guild_id BIGINT,
    user_id BIGINT,
    PRIMARY KEY (guild_id, user_id),
    FOREIGN KEY (guild_id) REFERENCES antinuke_settings (guild_id)
);
CREATE TABLE IF NOT EXISTS joindm_settings (
    guild_id BIGINT PRIMARY KEY,
    message TEXT
);
CREATE TABLE IF NOT EXISTS prefixes (
    user_id TEXT PRIMARY KEY,
    prefix TEXT
);
