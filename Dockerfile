FROM python:3.8

WORKDIR /mafia

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Set the environment variables for the server port
ENV SERVER_PORT=50051

# Expose the server port
EXPOSE ${SERVER_PORT}

# Run the application
CMD [ "python", "server_main.py" ]