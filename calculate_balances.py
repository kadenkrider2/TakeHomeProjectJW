import csv
from collections import defaultdict
from datetime import datetime
from typing import Any


# noinspection typechecker,PyTypeChecker
def calculate_balances(transactions_file):
    # Create a dictionary to store the balances for each customer
    balances: defaultdict[Any, int] = defaultdict(int)

    # Create a dictionary to store the minimum, maximum, and ending balances for each customer and month
    monthly_balances = defaultdict(lambda: defaultdict(lambda: {'min': float('inf'), 'max': float('-inf'), 'end': 0}))

    # Initialize the results list
    results = []

    # Open the transactions file to read the transactions
    try:
        with open(transactions_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # skips the header row

            # Check that the header row is correct
            if header != ['customer_id', 'date', 'amount']:
                raise ValueError('Incorrect header row in transactions file')

            # sort transactions by date and type
            sorted(reader,
                   key=lambda x: (datetime.strptime(x[1],
                                                    '%m/%d/%Y').date(), x[2]))

            # Iterate through each transaction
            for row in reader:
                # Get the customer ID, date, and amount for the transaction
                customer_id = row[0]
                date = datetime.strptime(row[1], '%m/%d/%Y').date()
                amount = int(row[2])

                if amount <= 0:
                    pass
                # process credit transactions before debit
                else:

                    balances[customer_id] += amount
            else:

                # update balances for the customer
                amount *= -1

                # Get the month and year for the transaction
                month = date.month
                year = date.year

                # Update the minimum, maximum, and ending balances for the customer and month
                monthly_balances[customer_id][(month, year)]['min'] = min(balances[customer_id],
                                                                          monthly_balances[customer_id][[month, year]][
                                                                              'min'])
                monthly_balances[customer_id][(month, year)]['max'] = max(balances[customer_id],
                                                                          monthly_balances[customer_id][(month, year)][
                                                                              'max'])
                monthly_balances[customer_id][(month, year)]['end'] = balances[customer_id]

    except IOError:
        print(f"Unable to open transactions file: {transactions_file}")
        return []
    except ValueError as e:
        print(e)
        return []

    # Format the results and add them to the results list
    for customer_id in monthly_balances:
        for (month, year) in monthly_balances[customer_id]:
            min_balance = monthly_balances[customer_id][(month, year)]['min']
            max_balance = monthly_balances[customer_id][(month, year)]['max']
            end_balance = monthly_balances[customer_id][(month, year)]['end']
            results.append(f"{customer_id}, {month}/{year}, {min_balance}, {max_balance}, {end_balance}")

    return results
