# Use ARM64 Linux image (native on Apple Silicon)
FROM --platform=linux/arm64 debian:bullseye-slim

# Install build tools
RUN apt-get update && \
    apt-get install -y build-essential autoconf automake libtool pkg-config wget tar && \
    rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy tar.gz into container
COPY kingfisher.tar.gz /app/

# Extract tar.gz and build
RUN tar -xzf kingfisher.tar.gz && \
    make   # assumes there's a Makefile

# Default command to run the binary
CMD ["./kingfisher"]   # replace with actual binary name if different

