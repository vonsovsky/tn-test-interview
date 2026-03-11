# Number List Operator Program
This program performs various operations on a list of numbers
based on the specified operator. Program is designed like infinite
loop which you can exit by pressing `Ctrl + C` in your terminal or using `exit` or `quit`.
You can send request thats will be processed by the program and it will return the result based on the operator you choose.

Request is always in the format: `numbers operator [additional parameters]` where 
`numbers` is a list of numbers separated by space, 
`operator` is the operation you want to perform and 
`additional parameters` are optional parameters required for some operators. (see section input)

Program has implemented logging, so you can set logging level 
to see more or less details about the program execution.
By default, logging level is set to `INFO`.

Program is able to hold 3 tasks in the queue. When the queue is full, it will reject new tasks until there is space in the queue.

## running program 
To run the program, use the following command in your terminal:
```bash
python main.py
```
To set logging level, use the following command:
```bash
python main.py --log-level <level>
```
Where `<level>` can be one of the following: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

## input 
Program expects list of numbers, operator and aditional parameters for some operators.

| Operator | Description | Additional Parameters |
|----------|-------------|----------------------|
| `sum` | Sums all numbers in the list. | None |
| `add` | Adds a specified number to each element in the list. | `number` (the number to add) |
| `multiply` | Multiplies all elements in the list | None |
| `multiply_by` | Multiplies each element in the list by a specified number. | `number` (the number to multiply by) |
| `send_first` | Sends the first element of the list to the whole list | None |


### example inputs and outputs
|                      |
|----------------------|
| 1 2 3 4 5 sum -> 15  |
|1 2 3 4 5 add 10 -> 11 12 13 14 15|
|1 2 3 4 5 multiply -> 120|
|1 2 3 4 5 multiply_by 10 -> 10 20 30 40 50|
|1 2 3 4 5 send_first -> 1 1 1 1 1|

