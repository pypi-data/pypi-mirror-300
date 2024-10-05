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
        + await Pu.get_text(
            page, "//h3[contains(text(),'Overview')]/following-sibling::div[2] "
        )
    )
    typ = await Pu.get_text(
        page, "//div[*[text()='Project ID:']]/preceding-sibling::div[1]/div[1]"
    )

    status = await Pu.get_text(page, "img[alt='Profile'] + span")
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
    await page.wait_for_selector("div#project-section-container")

    buyer_agency = await Pu.get_text(page, ".contact-section p:has(strong)")
    buyer_agency = buyer_agency.split(":")[-1] if buyer_agency else None
    buyer_agency = (
        buyer_agency if buyer_agency else await Pu.get_text(page, "div:has(> i.fa-university)")
    )
    buyer_name = await Pu.get_text(page, ".contact-section strong")
    buyer_name = (
        buyer_name
        if buyer_name
        else await Pu.get_text(
            page, "span[data-templatevariable*='procurementFullName']"
        )
    )
    buyer_email = await Pu.get_text(page, ".contact-section a[href^='mailto:']")
    buyer_phone = await Pu.get_text(page, ".contact-section a[href^='tel:']")

    pre_bid_element = await page.query_selector(".timeline-group")
    if pre_bid_element:
        pre_proposal_time = await Pu.get_text(
            page, ".timeline-group .col-md-6:nth-child(2)"
        )
        pre_proposal_time = pre_proposal_time.split("\n")[0].strip()

        pre_proposal_description = await Pu.get_text(
            page, ".timeline-group .col-md-6:nth-child(2) div"
        )
        pre_proposal_description = pre_proposal_description.strip()
    else:
        pre_proposal_time = None
        pre_proposal_description = None

    pre_proposal_description = (
        pre_proposal_description
        if pre_proposal_description
        else await Pu.get_text(page, 'td:has-text("Pre-Bid Meeting") + td')
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
            "pre_proposal_description": pre_proposal_description,
            "solicitation_stage": None,
            "attachments": files,
            "industry_items": p_items,
        }
    )
