# Models

The application uses the following database models:

## Question Table

```sql
CREATE TABLE Question (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);
```


## Students Table

```sql
CREATE TABLE Student (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    program VARCHAR(100) NOT NULL,
    branch VARCHAR(100) NOT NULL
);
```


## Mark Table

```sql
CREATE TABLE Mark (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    marks INTEGER NOT NULL,
    year INTEGER NOT NULL DEFAULT (strftime('%Y', 'now')),
    student_id VARCHAR(20) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);
```


## Solved Table

```sql
CREATE TABLE Solved (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    student_id VARCHAR(50) NOT NULL,
    remarks TEXT,
    marks INTEGER NOT NULL,
    link1 VARCHAR(200),
    link2 VARCHAR(200),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```





