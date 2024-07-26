from flask import Flask, jsonify, abort, request
from flasgger import Swagger
from rpn.stack import Stack

app = Flask(__name__)

swagger = Swagger(app, template= { "info": { "title": "RPN Stack API" } })

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
    """
    List all available operands
    ---
    responses:
      200:
        description: A list of available operands
        schema:
          type: array
          items:
            type: string
    """
    return jsonify(list(OPERANDS.keys()))

@app.route("/rpn/stacks")
def list_stacks():
    """
    List all stacks
    ---
    responses:
      200:
        description: A list of all stacks
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              stack:
                type: array
                items:
                  type: number
    """
    stack_list = [
      stack.to_dict() for stack in stacks.values()
    ]

    return stack_list

@app.route("/rpn/stacks/<int:id>")
def get_stack(id):
    """
    Get a stack by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The stack ID
    responses:
      200:
        description: The stack data
        schema:
          type: object
          properties:
            id:
              type: integer
            stack:
              type: array
              items:
                type: number
      404:
        description: Stack not found
    """
    if id in stacks:
        stack = stacks[id]
        return stack.to_dict()
    else:
        stackNotFound()

@app.route("/rpn/stacks", methods=['POST'])
def create_stack():
    """
    Create a new stack
    ---
    responses:
      201:
        description: The created stack
        schema:
          type: object
          properties:
            id:
              type: integer
            stack:
              type: array
              items:
                type: number
    """
    stack = Stack()
    stacks[stack.id] = stack

    return stack.to_dict(), 201

@app.route("/rpn/stacks/<int:id>", methods=['DELETE'])
def delete_stack(id):
    """
    Delete a stack by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The stack ID
    responses:
      204:
        description: Stack deleted
      404:
        description: Stack not found
    """
    if id in stacks:
        del stacks[id]
        return '', 204
    else:
        stackNotFound()

@app.route("/rpn/stacks/<int:id>", methods=['POST'])
def push_to_stack(id):
    """
    Push a value to a stack
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The stack ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            value:
              type: number
    responses:
      200:
        description: The updated stack
        schema:
          type: object
          properties:
            id:
              type: integer
            stack:
              type: array
              items:
                type: number
      400:
        description: Invalid input
      404:
        description: Stack not found
    """
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
    """
    Apply an operand to a stack
    ---
    parameters:
      - name: op
        in: path
        type: string
        required: true
        description: The operand
      - name: id
        in: path
        type: integer
        required: true
        description: The stack ID
    responses:
      200:
        description: The result of the operation and the updated stack
        schema:
          type: object
          properties:
            result:
              type: number
            stack:
              type: object
              properties:
                id:
                  type: integer
                stack:
                  type: array
                  items:
                    type: number
      400:
        description: Invalid input or unsupported operation
      404:
        description: Stack not found
    """
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
