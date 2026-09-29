from ui.application import KrishApplication


def main():

    application = KrishApplication()

    raise SystemExit(
        application.run()
    )


if __name__ == "__main__":
    main()