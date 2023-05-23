import uvicorn

from password_cracker_minion import minion_context


def main():
    """
    main is the main function
    :return:
    """
    print("Hello World!")


if __name__ == "__main__":
    main()
    uvicorn.run("password_cracker_minion.src.server:main_api_router", host=minion_context.main_settings.minion_host,
                port=minion_context.main_settings.minion_port, reload=True)
