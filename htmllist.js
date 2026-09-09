console.log(
  require("./users.json")
    .map(
      ({id, url}) =>
          "<li>" +
          `  <a href="${url}">${id.replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll("&", "&amp;")}</a>` +
          "</li>"
    )
    .join("")
)
