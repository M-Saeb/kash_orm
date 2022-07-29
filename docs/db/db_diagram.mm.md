---
markmap:
  maxWidth: 300
---

# DB Class

## Methods
- `create_model()`
- `update_model()`
- `delete_model()`
- `get_model()`
- `search_models()`

## Depends on

### `ModelReader`

#### Methods
- `get_columns()`
- `filter()`
- `create_record()`

#### Depends on

##### `RecordClass`
- `update()`
- `delete()`

### Model Writer

#### `ModelCreator`
- `create()`

#### `ModelUpdator`
- `create_columns()`
- `update_columns()`
- `delete_columns()`


