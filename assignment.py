"""
customerdata.txt contains transactional data from a fictitious website.
Parse it and generate a report with the following information

1. How many orders did the site receive?
2. What was the total amount of the orders?
3. List the names of the customers who ordered once and did not order again.
4. Get a distribution of customers who ordered exactly once, exactly twice,
  and so on up to 4 orders and group the rest as 5 orders and above
5. Generate this report as a simple HTML page with a table.
6. Add a bar graph for the information in Q4 in your HTML report.
"""
from os import getcwd


def structure_data():
    """
    Reads the customerdata.txt file and returns data structured as below
    {
        <phone_number>: {
            "name": <name>
            "orders": [
                {"date": <date>, "amount": <amount>},
                ..
                ..
            ]
        },
        ..
        ..
    }
    It also returns the total number and total amount of orders
    """
    with open("customerdata.txt") as f:
        f.readline()
        data = {}
        total_orders = 0
        total_amount = 0
        while True:
            try:
                date, phone_number, name, amount = f.readline().strip().split(", ")
                amount = int(amount)
                try:
                    # Neglect if there is a name mismatch for the same number
                    data[phone_number]["orders"].append(
                        {"date": date, "amount": amount}
                    )
                except KeyError:
                    data[phone_number] = {
                        "name": name,
                        "orders": [{"date": date, "amount": amount}],
                    }
                total_amount += amount
                total_orders += 1
            except ValueError:
                break
    return data, total_orders, total_amount


def group_customers(data):
    """
    Groups customers as per number of orders made

    Also collects names of customers who never reordered
    """
    groups = {"1": 0, "2": 0, "3": 0, "4": 0, "5+": 0}
    non_repeat_customers = []
    for value in data.values():
        orders_made = len(value["orders"])
        try:
            groups[str(orders_made)] += 1
        except KeyError:
            groups["5+"] += 1
        if orders_made == 1:
            non_repeat_customers.append(value["name"])
    return groups, non_repeat_customers


if __name__ == "__main__":
    data, total_orders, total_amount = structure_data()
    print(f"Total orders => {total_orders}")
    print(f"Total amount of orders => {total_amount}")

    groups, non_repeat_customers = group_customers(data)

    print(f"Customers who never reordered => {non_repeat_customers}")

    table = """
    <table width="100%" border=1>
        <tr>
            <th align="left">No of orders</th>
            <th align="left">Count of customers</th>
        </tr>
    """
    for number_of_orders, count in groups.items():
        table = (
            table
            + f"""
        <tr>
            <td>{number_of_orders}</td>
            <td>{count}</td>
        </tr>
        """
        )
    table = table + "</table>"

    bar_chart = '<table border="0" width="100%" cellpadding = "0" cellspacing="0">'
    for number_of_orders, count in groups.items():
        percentage = round((100 / len(data)) * count, 2)
        bar_chart = (
            bar_chart
            + f"""
        <tr>
          <td width="20%">{number_of_orders} order(s)</td>
          <td width="75%">
            <table border = "0" width = "100%" cellpadding = "1" cellspacing="1">
              <tr>
                <td align="left" bgcolor="blue" width="{percentage}%"> </td>
                <td align="left">{percentage}%</td>
              </tr>
            </table>
          </td>
        </tr>
        """
        )
    bar_chart = bar_chart + "</table>"

    with open("customerdata.html", "w") as f:
        f.write(
            f"""
            <h1>Distribution of customers who ordered exactly once, exactly twice, and so on up to 4 orders and the rest as 5 orders and above</h1>
            <br>
            <h2>Table:</h2>
            {table}
            <br>
            <h2>Bar chart:</h2>
            {bar_chart}
        """
        )
    print(f"HTML => Open file://{getcwd()}/{f.name}")
