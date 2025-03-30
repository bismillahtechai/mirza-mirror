CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS thoughts (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    source TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    audio_file TEXT,
    document_file TEXT,
    summary TEXT,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS tags (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS thought_tags (
    thought_id TEXT NOT NULL REFERENCES thoughts(id) ON DELETE CASCADE,
    tag_id TEXT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (thought_id, tag_id)
);

CREATE TABLE IF NOT EXISTS links (
    id TEXT PRIMARY KEY,
    source_thought_id TEXT NOT NULL REFERENCES thoughts(id) ON DELETE CASCADE,
    target_thought_id TEXT NOT NULL REFERENCES thoughts(id) ON DELETE CASCADE,
    relationship TEXT NOT NULL,
    strength FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS imported_conversations (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    format TEXT NOT NULL,
    original_file TEXT NOT NULL,
    imported_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS conversation_thoughts (
    conversation_id TEXT NOT NULL REFERENCES imported_conversations(id) ON DELETE CASCADE,
    thought_id TEXT NOT NULL REFERENCES thoughts(id) ON DELETE CASCADE,
    segment_index INTEGER NOT NULL,
    role TEXT NOT NULL,
    PRIMARY KEY (conversation_id, thought_id)
);

CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    file_path TEXT NOT NULL,
    content TEXT,
    content_type TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    docling_representation JSONB,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS actions (
    id TEXT PRIMARY KEY,
    thought_id TEXT NOT NULL REFERENCES thoughts(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    priority TEXT NOT NULL,
    due_date TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_thoughts_created_at ON thoughts(created_at);
CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name);
CREATE INDEX IF NOT EXISTS idx_links_source ON links(source_thought_id);
CREATE INDEX IF NOT EXISTS idx_links_target ON links(target_thought_id);
CREATE INDEX IF NOT EXISTS idx_conversation_thoughts_conversation ON conversation_thoughts(conversation_id);
CREATE INDEX IF NOT EXISTS idx_actions_thought ON actions(thought_id);
CREATE INDEX IF NOT EXISTS idx_actions_completed ON actions(completed);
