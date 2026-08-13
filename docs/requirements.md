# Balanzo Requirements

## 1. Project Overview

Balanzo is a personal finance analytics platform designed to help users track, analyze, and understand their spending behavior.

## 2. Target User

The primary user is an individual who wants to monitor their personal income and expenses.

## 3. MVP Features

### Transaction Management

- Create transaction
- View transaction
- Update transaction
- Delete transaction

### Dashboard

- View total income
- View total expenses
- View current balance

### Analytics

- Analyze expenses by category
- Analyze monthly spending
- Calculate average spending
- Identify top spending categories

### Insight

- Generate basic spending insights
- Compare spending between periods

## 4. Transaction Data

Each transaction contains:

- User
- Category
- Amount
- Type
- Description
- Transaction date

## 5. Transaction Types

- Income
- Expenses

## 6. Main Entities

- User
- Category
- Transaction

## 7. Database Entities

### Users

Stores user account information.

Attributes: 

- id
- name
- email
- password
- created_at
- update_at

### Categories

Stores transaction categories.

Attributes:

- id
- name
- type
- created_at
- update_at

Category types:

- income
- expense

### Transactions

Stores financial transactions.

Attributes:

- id
- user_id
- category_id
- amount
- description
- transaction_date
- created_at
- updated_at

## 8. Relationships

- One user can have many transactions.
- One category can be associated with many transactions.
- Each transaction belongs to one user.
- Each transaction belongs to one category.