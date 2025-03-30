# Database Schema Design

## Tables

### thoughts
- id: UUID (primary key)
- content: TEXT
- source: ENUM ('voice_note', 'text_note', 'chat', 'import')
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
- audio_file: TEXT (nullable)
- embedding_id: UUID (foreign key to embeddings)
- summary: TEXT (nullable)
- metadata: JSONB

### embeddings
- id: UUID (primary key)
- vector: VECTOR
- created_at: TIMESTAMP

### tags
- id: UUID (primary key)
- name: TEXT
- type: ENUM ('project', 'emotion', 'category', 'custom')
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### thought_tags
- thought_id: UUID (foreign key to thoughts)
- tag_id: UUID (foreign key to tags)
- confidence: FLOAT
- created_at: TIMESTAMP
- PRIMARY KEY (thought_id, tag_id)

### links
- id: UUID (primary key)
- source_thought_id: UUID (foreign key to thoughts)
- target_thought_id: UUID (foreign key to thoughts)
- relationship: ENUM ('similar', 'continuation', 'contradiction', 'inspiration')
- strength: FLOAT
- created_at: TIMESTAMP

### actions
- id: UUID (primary key)
- thought_id: UUID (foreign key to thoughts)
- content: TEXT
- status: ENUM ('pending', 'completed', 'dismissed')
- due_date: TIMESTAMP (nullable)
- priority: ENUM ('high', 'medium', 'low')
- created_at: TIMESTAMP
- updated_at: TIMESTAMP

### reflections
- id: UUID (primary key)
- type: ENUM ('insight', 'pattern', 'summary')
- content: TEXT
- created_at: TIMESTAMP

### reflection_thoughts
- reflection_id: UUID (foreign key to reflections)
- thought_id: UUID (foreign key to thoughts)
- created_at: TIMESTAMP
- PRIMARY KEY (reflection_id, thought_id)

## Indexes

- thoughts(created_at)
- thoughts(updated_at)
- thought_tags(tag_id)
- links(source_thought_id)
- links(target_thought_id)
- actions(thought_id)
- actions(status)
- actions(due_date)
- reflection_thoughts(thought_id)

## Constraints

- Foreign key constraints on all relationships
- Check constraints on enum fields
- Not null constraints on required fields
