from flask import Flask, jsonify, abort, request
from rpn.stack import Stack

app = Flask(__name__)

stacks = {}

OPERANDS = {
    '+': 'add',
    '-': 'subtract',
    '*': 'multiply',
    '/': 'divide',
}

def stackNotFound():
  abort(404, description="Stack not found")


@app.route("/rpn/op")
def list_operands():
    return jsonify(list(OPERANDS.keys()))

@app.route("/rpn/stacks")
def list_stacks():
    stack_list = [
      stack.to_dict() for stack in stacks.values()
    ]

    return stack_list

@app.route("/rpn/stacks/<int:id>")
def get_stack(id):
    if id in stacks:
        stack = stacks[id]
        return stack.to_dict()
    else:
        stackNotFound()

@app.route("/rpn/stacks", methods=['POST'])
def create_stack():
    stack = Stack()
    stacks[stack.id] = stack

    return stack.to_dict(), 201

@app.route("/rpn/stacks/<int:id>", methods=['DELETE'])
def delete_stack(id):
    if id in stacks:
        del stacks[id]
        return '', 204
    else:
        stackNotFound()

@app.route("/rpn/stacks/<int:id>", methods=['POST'])
def push_to_stack(id):
    if id in stacks:
        data = request.get_json()

        if not data or 'value' not in data:
            abort(400, description="Payload must be JSON and contain key 'value'")

        value = data['value']
        if not isinstance(value, (int, float)):
            abort(400, description="'value' must be a number")

        stack = stacks[id]
        stack.push(value)

        return stack.to_dict()
    else:
        stackNotFound()

@app.route("/rpn/op/<op>/stacks/<int:id>", methods=['POST'])
def apply_operand_to_stack(op, id):
    if id in stacks:
        if op in OPERANDS:
            stack = stacks[id]
            operation = OPERANDS[op]
            try:
                result = getattr(stack, operation)()
            except ValueError as e:
                abort(400, description=str(e))
            except ZeroDivisionError as e:
                abort(400, description=str(e))

            return jsonify({'result': result, 'stack': stack.to_dict()})
        else:
            abort(400, description="Unsupported operation")
    else:
        stackNotFound()
