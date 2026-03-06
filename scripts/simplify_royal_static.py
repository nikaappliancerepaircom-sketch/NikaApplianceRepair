from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup, Comment


TARGET_DIR = Path(r"c:\NikaApplianceRepair\Royal Garagedoors OLD")
STATIC_ASSET_HREF = "/assets/static-site.css"
STATIC_SCRIPT_SRC = "/assets/site.js"
RTMICON_REGULAR = "./rtmicon-regular.css"
RTMICON_THIN = "./rtmicon-thin.css"

LINK_REMOVE_MATCHES = (
    "gmpg.org",
    "xmlrpc.php",
    "wlwmanifest",
    "api.w.org",
    "wp-json/oembed",
)
META_REMOVE_NAMES = {
    "generator",
    "facebook-domain-verification",
}
SCRIPT_KEEP_SRC = {
    STATIC_SCRIPT_SRC,
}


def ensure_static_assets() -> None:
    assets_dir = TARGET_DIR / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    (assets_dir / "site.js").write_text(
        """document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;

  document.querySelectorAll(".elementskit-menu-toggler").forEach((button) => {
    const nav = button.closest("nav");
    const container = nav?.querySelector(".elementskit-menu-container");
    const overlay = nav?.querySelector(".elementskit-menu-overlay");

    if (!container) {
      return;
    }

    const closeMenu = () => {
      container.classList.remove("is-open");
      overlay?.classList.remove("is-open");
      body.classList.remove("menu-open");
      button.setAttribute("aria-expanded", "false");
    };

    button.addEventListener("click", () => {
      const isOpen = container.classList.toggle("is-open");
      overlay?.classList.toggle("is-open", isOpen);
      body.classList.toggle("menu-open", isOpen);
      button.setAttribute("aria-expanded", String(isOpen));
    });

    overlay?.addEventListener("click", closeMenu);

    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        if (window.innerWidth <= 1024) {
          closeMenu();
        }
      });
    });
  });

  document.querySelectorAll(".ekit-accordion--toggler").forEach((trigger) => {
    const targetSelector = trigger.getAttribute("data-target") || trigger.getAttribute("href");
    const target = targetSelector ? document.querySelector(targetSelector) : null;

    if (!target) {
      return;
    }

    trigger.addEventListener("click", (event) => {
      event.preventDefault();
      const isOpen = target.classList.contains("show");

      trigger
        .closest(".elementskit-card")
        ?.parentElement
        ?.querySelectorAll(".collapse.show")
        .forEach((panel) => panel.classList.remove("show"));

      trigger
        .closest(".elementskit-card")
        ?.parentElement
        ?.querySelectorAll(".ekit-accordion--toggler")
        .forEach((item) => item.classList.add("collapsed"));

      if (!isOpen) {
        target.classList.add("show");
        trigger.classList.remove("collapsed");
      }
    });
  });

  document.querySelectorAll("form[data-static-form='true']").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();

      if (typeof form.reportValidity === "function" && !form.reportValidity()) {
        return;
      }

      window.location.href = "/thank-you/";
    });
  });
});
""",
        encoding="utf-8",
    )

    (assets_dir / "static-site.css").write_text(
        """body.menu-open {
  overflow: hidden;
}

.elementor-g-recaptcha,
script,
noscript iframe {
  display: none !important;
}

@media (max-width: 1024px) {
  .elementskit-menu-container {
    display: none;
  }

  .elementskit-menu-container.is-open {
    display: block;
  }

  .elementskit-menu-overlay {
    display: none;
  }

  .elementskit-menu-overlay.is-open {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    z-index: 998;
  }

  .elementskit-menu-container.is-open {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    width: min(88vw, 360px);
    overflow-y: auto;
    background: #ffffff;
    z-index: 999;
    padding: 24px 20px 32px;
    box-shadow: -18px 0 48px rgba(0, 0, 0, 0.18);
  }
}

.collapse {
  display: none;
}

.collapse.show {
  display: block;
}
""",
        encoding="utf-8",
    )

    (assets_dir / "rtmicon-regular.css").write_text("/* Static stub for removed plugin icon import. */\n", encoding="utf-8")
    (assets_dir / "rtmicon-thin.css").write_text("/* Static stub for removed plugin icon import. */\n", encoding="utf-8")


def should_remove_link(tag) -> bool:
    href = tag.get("href", "")
    rel = {value.lower() for value in tag.get("rel", [])}
    if "profile" in rel:
        return True
    if "alternate" in rel and "rss+xml" in (tag.get("type", "") or ""):
        return True
    return any(match in href for match in LINK_REMOVE_MATCHES)


def process_html_file(path: Path) -> None:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    for link in soup.find_all("link"):
        if not getattr(link, "attrs", None):
            continue
        delayed = link.get("data-pmdelayedstyle")
        if delayed:
            link["href"] = delayed
            del link["data-pmdelayedstyle"]

        href = link.get("href", "")
        if href == RTMICON_REGULAR:
            link["href"] = "/assets/rtmicon-regular.css"
        elif href == RTMICON_THIN:
            link["href"] = "/assets/rtmicon-thin.css"

        if should_remove_link(link):
            link.decompose()

    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        if name in META_REMOVE_NAMES:
            meta.decompose()

    for noscript in soup.find_all("noscript"):
        content = str(noscript)
        if "googletagmanager" in content or "perfmatters-lazy" in content:
            noscript.decompose()

    for script in soup.find_all("script"):
        src = script.get("src")
        if src in SCRIPT_KEEP_SRC:
            continue
        script.decompose()

    for recaptcha in soup.select(".elementor-g-recaptcha"):
        recaptcha.decompose()

    for form in soup.find_all("form"):
        form["action"] = "/thank-you/"
        form["method"] = "post"
        form["data-static-form"] = "true"

        for node in form.select(".elementor-field-type-recaptcha_v3"):
            node.decompose()

        for hidden in form.find_all("input", attrs={"type": "hidden"}):
            hidden.decompose()

    for tag in soup.find_all(True):
        for attr in ("href", "src", "action", "data-settings", "onclick"):
            value = tag.get(attr)
            if not value:
                continue

            text = str(value)
            if "/wp-admin/admin-ajax.php" in text or "/wp-json/" in text:
                if attr in {"href", "src", "action"}:
                    tag[attr] = "#"
                else:
                    del tag[attr]

        target = tag.get("data-target")
        if target and target.startswith("#Collapse-"):
            tag["data-target"] = target

    head = soup.head
    if head and not head.find("link", href=STATIC_ASSET_HREF):
        css_tag = soup.new_tag("link", rel="stylesheet", href=STATIC_ASSET_HREF)
        head.append(css_tag)

    body = soup.body
    if body and not body.find("script", src=STATIC_SCRIPT_SRC):
        script_tag = soup.new_tag("script", src=STATIC_SCRIPT_SRC, defer=True)
        body.append(script_tag)

    html = str(soup)
    html = html.replace(RTMICON_REGULAR, "/assets/rtmicon-regular.css")
    html = html.replace(RTMICON_THIN, "/assets/rtmicon-thin.css")
    for closing_tag in ("</link>", "</meta>", "</img>", "</input>", "</br>", "</hr>"):
        html = html.replace(closing_tag, "")
    path.write_text(html, encoding="utf-8")


def main() -> None:
    ensure_static_assets()
    for html_file in TARGET_DIR.rglob("*.html"):
        process_html_file(html_file)


if __name__ == "__main__":
    main()
