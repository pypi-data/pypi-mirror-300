# earthquake-detection-indonesia
This package will get the latest earthquake form BMKG (Agency from Indonesia)
[LICENSE](LICENSE)

## How Its Works?
This package will scrape from [BMKG](https://bmkg.go.id) to get latest earthquake happened in Indonesia

This package will use BeautifulSoup4 and Request, to produce output in the form of JSON that is raedy to be used in web or mobile application

## How To Use

```
import gempaterkini

if __name__ == "__main__":
    print("Aplikasi Utama")
    result = gempaterkini.ekstraksi_data()
    gempaterkini.tampilkan_data(result)
```

## Author
Gugun M Fauzi