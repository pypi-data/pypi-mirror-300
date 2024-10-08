ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}
COPY . ./app/
WORKDIR /app
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="${PATH}:/root/.cargo/bin"
RUN cargo install --locked maturin
