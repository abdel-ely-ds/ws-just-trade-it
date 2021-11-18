import uvicorn

entry_point = "app:app"


def main():
    uvicorn.run(entry_point, host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    main()
