from os.path import join as joinpath
from json import load
from os import mkdir
from shutil import rmtree as rmdir

SITES_DIRECTORY = "sites"
USE_FILETYPE = "xhtml"

SITES: dict[str, dict] = {}
with open("users.json") as file:
    SITES = load(file)

BringUserToSite = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta charset="utf-8" />
    <meta http-equiv="refresh" content="0; url={{siteurl}}" />
    <link rel="canonical" href="{{siteurl}}" />
    <title>Bringing you to {{siteid}}</title>
    <style type="text/css">
    html {
        background-color: #000;
        color: #fff;
    }
    a {
        color: #0af;
        text-decoration: underline;
    }
    </style>
</head>

<body>
    <h1>Bringing You Somewhere Else...</h1>
    <p>
        Uh-Oh! If you're seeing this, the page has failed to
        bring you to <a href="{{siteurl}}">{{siteid}}</a>'(s)
        site!
    </p>
    <p>
        To be taken there, use the following URL:
    </p>
    <p>
        <a href="{{siteurl}}">{{siteurl}}</a>
    </p>
    <script type="application/javascript">
        if (window && window.location && window.location.replace) {
            window.location.replace("{{siteurl}}");
        } else if (window && window.location) {
            windows.location = "{{siteurl}}";
        }
    </script>
    <!--
        This all _should_ work in basically
        every browser and search crawler that
        has ever existed.
    -->
</html>
"""

def main():
    try:
        rmdir(SITES_DIRECTORY)
        print("Reinitalizing sites directory")
    except:
        print("Creating sites directory")
    mkdir(SITES_DIRECTORY)

    for index, cursite in enumerate(SITES):
        print("Creating site directory for %s" % cursite["id"])
        maker = lambda site: BringUserToSite.replace("{{siteid}}", site["id"]).replace("{{siteurl}}", site["url"])
        NextIndex = index + 1 if index + 1 < len(SITES) else 0
        PrevIndex = index - 1 if index - 1 > 0 else len(SITES) - 1
        Next = maker(NextIndex)
        Prev = maker(PrevIndex)
        mkdir(joinpath(SITES_DIRECTORY, cursite["id"]))
        with open(joinpath(SITES_DIRECTORY, cursite["id"], "next.%s" % USE_FILETYPE) as file:
            file.write(Next)
        with open(joinpath(SITES_DIRECTORY, cursite["id"], "prev.%s" % USE_FILETYPE) as file:
            file.write(Prev)
    print("Finished making sites directory")

if __name__ == "__main__":
    main()
