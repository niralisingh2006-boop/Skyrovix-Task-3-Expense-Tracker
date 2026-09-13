from datetime import date
from .db import connect,init_db,seed
def money(x):return f'₹{x:,.2f}'
def cats(c):return c.execute('SELECT * FROM categories ORDER BY name').fetchall()
def choose(c):
 rows=cats(c)
 for x in rows:print(x['id'],x['name'])
 while 1:
  try:
   i=int(input('Category ID: '));
   if any(x['id']==i for x in rows):return i
  except ValueError:pass
  print('Invalid category.')
def add(c):
 try:
  a=float(input('Amount: ')); assert a>0
 except (ValueError,AssertionError):print('Amount must be positive.');return
 i=choose(c);d=input('Description: ').strip();dt=input(f'Date [{date.today()}]: ').strip() or str(date.today())
 if not d:print('Description cannot be empty.');return
 try:date.fromisoformat(dt)
 except ValueError:print('Invalid date.');return
 c.execute('INSERT INTO expenses(amount,category_id,description,expense_date) VALUES(?,?,?,?)',(a,i,d,dt));c.commit();print('Expense added.')
def listing(c):
 rows=c.execute('SELECT e.*,c.name category FROM expenses e JOIN categories c ON c.id=e.category_id ORDER BY expense_date DESC,id DESC').fetchall()
 if not rows:print('No expenses found.')
 for x in rows:print(x['id'],x['expense_date'],x['category'],money(x['amount']),x['description'])
def update(c):
 listing(c)
 try:
  i=int(input('Expense ID: ')); a=float(input('New amount: ')); assert a>0
 except (ValueError,AssertionError): print('Invalid ID or amount.'); return
 cat=choose(c); d=input('New description: ').strip(); dt=input('New date YYYY-MM-DD: ').strip()
 if not d: print('Description cannot be empty.'); return
 try: date.fromisoformat(dt)
 except ValueError: print('Invalid date.'); return
 q=c.execute('UPDATE expenses SET amount=?,category_id=?,description=?,expense_date=? WHERE id=?',(a,cat,d,dt,i)); c.commit(); print('Expense updated.' if q.rowcount else 'Expense not found.')
def delete(c):
 listing(c)
 try:i=int(input('Expense ID: '))
 except ValueError:print('Invalid ID.');return
 q=c.execute('DELETE FROM expenses WHERE id=?',(i,));c.commit();print('Deleted.' if q.rowcount else 'Not found.')
def budget(c):
 m=input('Month YYYY-MM: ').strip()
 try:date.fromisoformat(m+'-01');a=float(input('Budget amount: '));assert a>0
 except (ValueError,AssertionError):print('Invalid month or amount.');return
 c.execute('INSERT INTO budgets(month,amount) VALUES(?,?) ON CONFLICT(month) DO UPDATE SET amount=excluded.amount',(m,a));c.commit();print('Budget saved.')
def report(c):
 m=input('Month YYYY-MM [current]: ').strip() or date.today().strftime('%Y-%m');t=c.execute("SELECT COALESCE(SUM(amount),0) x FROM expenses WHERE substr(expense_date,1,7)=?",(m,)).fetchone()['x'];print('Total:',money(t))
 b=c.execute('SELECT amount FROM budgets WHERE month=?',(m,)).fetchone()
 if b:print('Budget alert: limit exceeded.' if t>b['amount'] else 'Remaining:',money(abs(b['amount']-t)))
def run():
 c=connect();init_db(c);seed(c);acts={'1':add,'2':listing,'3':update,'4':delete,'5':budget,'6':report}
 while 1:
  print('\n1 Add  2 List  3 Update  4 Delete  5 Budget  6 Report  7 Exit');x=input('Choose: ').strip()
  if x=='7':c.close();break
  if x in acts:acts[x](c)
  else:print('Invalid choice.')
