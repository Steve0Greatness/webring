from os.path import join as joinpath
from json import load
from os import mkdir
from shutil import rmtree as rmdir

SITES_DIRECTORY = "sites"
USE_FILETYPE = "xhtml"

SITES: dict[str, dict] = {}
with open("users.json") as file:
    SITES = load(file)

TEMP_REMOVE_SITES: dict[str, dict] = {}
with open("temprem.json") as file:
    TEMP_REMOVE_SITES = load(file)

# Below is XHTML because it is
BringUserToSite = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="refresh" content="0; url={{siteurl}}" />
    <link rel="canonical" href="{{siteurl}}" />
    <title>Bringing you to {{siteid}}</title>
    <style type="text/css">
    /*<![CDATA[*/
    html {
        background-color: #000;
        color: #fff;
    }
    a {
        color: #0af;
        text-decoration: underline;
    }
    /*]]>*/
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
        //<![CDATA[
        if (window && window.location && window.location.replace) {
            window.location.replace("{{siteurl}}");
        } else if (window && window.location) {
            windows.location = "{{siteurl}}";
        }
        //]]>
    </script>
    <!--
        This all _should_ work in basically
        every browser and search crawler that
        has ever existed.
    -->
</body>

</html>
"""
TempRemNotification = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <title>Temp. Removal: {{siteid}}</title>
    <style type="text/css">
    /*<![CDATA[*/
    html {
        background-color: #000;
        color: #fff;
    }
    a {
        color: #0af;
        text-decoration: underline;
    }
    /*]]>*/
    </style>
</head>

<body>
    <h1>{{siteid}} has been temporarily removed from the webring</h1>
    <p>
        This site has temporarily been removed by the webring owner.
        The given reason is:
    </p>
    <blockquote>{{reason}}</blockquote>
    <p>
        If you are {{siteid}}, please contact the webring
        owner to have your site reinstated; otherwise, let {{siteid}}
        know of this removal if possible.
    </p>
    <p>
        <a href="{{siteurl}}">Here's a link back to {{siteid}} if
        you need one</a>
    </p>
</body>

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
        print("Creating site redirect for %s" % cursite["id"])
        maker = lambda site: BringUserToSite.replace("{{siteid}}", site["id"]).replace("{{siteurl}}", site["url"])
        NextIndex = index + 1 if index + 1 < len(SITES) else 0
        PrevIndex = index - 1 if index - 1 >= 0 else len(SITES) - 1
        Next = maker(SITES[NextIndex])
        Prev = maker(SITES[PrevIndex])
        mkdir(joinpath(SITES_DIRECTORY, cursite["id"]))
        with open(joinpath(SITES_DIRECTORY, cursite["id"], "next.%s" % USE_FILETYPE), "x") as file:
            file.write(Next)
        with open(joinpath(SITES_DIRECTORY, cursite["id"], "prev.%s" % USE_FILETYPE), "x") as file:
            file.write(Prev)
    for index, cursite in enumerate(TEMP_REMOVE_SITES):
        print("Creating notice for %s" % cursite["id"])
        site = TempRemNotification.replace("{{siteid}}", cursite["id"]).replace("{{reason}}", cursite["reason"]).replace("{{siteurl}}", cursite["url"])
        mkdir(joinpath(SITES_DIRECTORY, cursite["id"]))
        with open(joinpath(SITES_DIRECTORY, cursite["id"], "next.%s" % USE_FILETYPE), "x") as file:
            file.write(site)
        with open(joinpath(SITES_DIRECTORY, cursite["id"], "prev.%s" % USE_FILETYPE), "x") as file:
            file.write(site)
    print("Finished making sites directory")

if __name__ == "__main__":
    main()
