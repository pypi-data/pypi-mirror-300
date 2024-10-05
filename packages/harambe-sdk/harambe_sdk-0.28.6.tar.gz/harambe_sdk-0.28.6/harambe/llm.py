async def scrape(sdk: SDK, current_url: str, *args: Any, **kwargs: Any) -> None:
    page: Page = sdk.page
    await page.wait_for_selector("#AppContent")

    post_title = await Pu.get_text(page, "div.panel-body h1")
    notice_id = await Pu.get_text(page, "//strong[text()='Project ID:']/parent::div")
    notice_id = notice_id.split(":")[-1].strip()
    desc = (
        await Pu.get_text(
            page,
            "//h3[contains(text(),'Overview')]/following-sibling::div[1]/div[last()]",
        )
        + "\n"
        + await Pu.get_text(page, "//h3[contains(text(),'Overview')]/following-sibling::div[2]")
    )
    typ = await Pu.get_text(
        page, "//div[*[text()='Project ID:']]/preceding-sibling::div[1]/div[1]"
    )

    status = await Pu.get_text(page, "img[alt='Profile'] + span")
    pre_proposal_time_element = await page.query_selector(
        "//div[contains(text(),'Pre-Proposal Meeting')]/following-sibling::div"
    )
    if pre_proposal_time_element:
        pre_proposal_time = (await pre_proposal_time_element.inner_text()).split("\n")[
            0
        ]
    else:
        pre_proposal_time = None
    open_date = (
        (await Pu.get_text(page, "//strong[text()='Release Date: ']/parent::div"))
        .split("Date:")[-1]
        .strip()
    )
    due_date = (
        (await Pu.get_text(page, "//strong[text()='Due Date:']/parent::div"))
        .split("Date:")[-1]
        .strip()
    )

    await page.click("a[data-qa=navbar-navItem-projectDocuments]")
    buyer_agency = None
    buyer_name = await Pu.get_text(
        page, "span[data-templatevariable*='procurementFullName']"
    )
    if not buyer_name:
        buyer_name = await Pu.get_text(
            page, "div.contact-section > strong:nth-of-type(1)"
        )
    buyer_email = await Pu.get_text(
        page, "span[data-templatevariable*='procurementEmail']"
    )
    if not buyer_email:
        buyer_email = await Pu.get_link(
            page, "div.contact-section > a:nth-of-type(1)"
        )
    buyer_phone = await Pu.get_text(
        page, "span[data-templatevariable*='procurementPhoneComplete']"
    )
    if not buyer_phone:
        buyer_phone = await Pu.get_link(
            page, "div.contact-section > a:nth-of-type(2)"
        )
    p_items = []
    try:
        await page.click("//span[text()='show all']", timeout=2000)
        await page.wait_for_timeout(1000)
    except TimeoutError:
        pass
    items = await page.query_selector_all(
        "//div[*[text()='Project ID:']]/preceding-sibling::div[1]/div[last()]/span/span"
    )
    for item in items[1:]:
        code = await item.inner_text()
        await item.hover()
        await page.wait_for_timeout(500)
        await page.wait_for_selector(
            "//div[contains(text(),'NIGP')] | //div[contains(text(),'UNSPSC')] | //div[contains(text(),'NAICS')]",
            timeout=2000,
        )
        code_desc = await (
            await page.query_selector(
                "//div[contains(text(),'NIGP')] | //div[contains(text(),'UNSPSC')] | //div[contains(text(),'NAICS')]"
            )
        ).inner_text()
        p_items.append(
            {
                "code_type": code_desc.split(":")[0],
                "code": code,
                "code_description": code_desc.replace("NIGP: ", "")
                .replace("UNSPSC:", "")
                .replace("NAICS:", "")
                .strip(),
                "description": None,
            }
        )

    await page.click("a[data-qa=navbar-navItem-downloads]")
    await page.wait_for_selector("//h2[contains(text(),'Project Documents Download')]")
    files = []  # attachments need login
    await sdk.save_data(
        {
            "solicitation_id": notice_id,
            "title": post_title,
            "description": desc,
            "solicitation_type": typ,
            "posted_date": open_date,
            "due_date": due_date,
            "issuing_entity": buyer_agency,
            "contact_name": buyer_name,
            "contact_number": buyer_phone,
            "contact_email": buyer_email,
            "status": status,
            "pre_proposal_time": pre_proposal_time,
            "pre_proposal_description": None,
            "solicitation_stage": None,
            "attachments": files,
            "industry_items": p_items,
        }
    )
