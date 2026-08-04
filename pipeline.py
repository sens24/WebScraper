#combines scraper, transform, and load
import scraper
import transform
import load
def main():
    scraper.main()
    transform.main()
    load.main()


if __name__ == "__main__":
    main()