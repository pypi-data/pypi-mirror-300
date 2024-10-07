"""
Tools for interacting with the VWS (Vuforia Web Services) website.
"""

import contextlib
import time
from typing import TypedDict

import click
import yaml
from beartype import beartype
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


@beartype
class DatabaseDict(TypedDict):
    """
    A dictionary type which represents a database.
    """

    database_name: str
    server_access_key: str
    server_secret_key: str
    client_access_key: str
    client_secret_key: str


@beartype
def log_in(
    driver: WebDriver,
    email_address: str,
    password: str,
) -> None:  # pragma: no cover
    """
    Log in to Vuforia web services.
    """
    log_in_url = "https://developer.vuforia.com/vui/auth/login"
    driver.get(url=log_in_url)
    email_address_input_element = driver.find_element(
        by=By.ID,
        value="login_email",
    )
    email_address_input_element.send_keys(email_address)

    password_input_element = driver.find_element(
        by=By.ID,
        value="login_password",
    )
    password_input_element.send_keys(password)
    password_input_element.send_keys(Keys.RETURN)


@beartype
def wait_for_logged_in(driver: WebDriver) -> None:  # pragma: no cover
    """
    Wait for the user to be logged in.

    Without this, we sometimes get a redirect to a post-login page.
    """
    ten_second_wait = WebDriverWait(driver=driver, timeout=10)
    ten_second_wait.until(
        expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, "userNameInHeaderSpan"),
        ),
    )


@beartype
def create_license(
    driver: WebDriver,
    license_name: str,
) -> None:  # pragma: no cover
    """
    Create a license.
    """
    licenses_url = "https://developer.vuforia.com/vui/develop/licenses"
    driver.get(url=licenses_url)

    ten_second_wait = WebDriverWait(driver=driver, timeout=10)

    ten_second_wait.until(
        expected_conditions.presence_of_element_located(
            (By.ID, "get-development-key"),
        ),
    )

    ten_second_wait.until(
        expected_conditions.element_to_be_clickable(
            (By.ID, "get-development-key"),
        ),
    )

    get_development_key_button_element = driver.find_element(
        by=By.ID,
        value="get-development-key",
    )
    get_development_key_button_element.click()
    try:
        get_development_key_button_element.click()
        time.sleep(1)
        get_development_key_button_element.click()
    except WebDriverException:
        pass

    license_name_input_element = ten_second_wait.until(
        expected_conditions.presence_of_element_located(
            (By.ID, "license-name"),
        ),
    )

    license_name_input_element.send_keys(license_name)

    agree_terms_id = "agree-terms-checkbox"
    agree_terms_checkbox_element = driver.find_element(
        by=By.ID,
        value=agree_terms_id,
    )
    agree_terms_checkbox_element.submit()


@beartype
def create_database(
    driver: WebDriver,
    database_name: str,
    license_name: str,
) -> None:  # pragma: no cover
    """
    Create a database.
    """
    target_manager_url = "https://developer.vuforia.com/vui/develop/databases"
    driver.get(url=target_manager_url)
    ten_second_wait = WebDriverWait(driver=driver, timeout=10)

    add_database_button_id = "add-dialog-btn"
    ten_second_wait.until(
        expected_conditions.presence_of_element_located(
            (By.ID, add_database_button_id),
        ),
    )

    ten_second_wait.until(
        expected_conditions.element_to_be_clickable(
            mark=(By.ID, add_database_button_id),
        ),
    )

    add_database_button_element = driver.find_element(
        by=By.ID,
        value=add_database_button_id,
    )
    add_database_button_element.click()
    with contextlib.suppress(WebDriverException):
        add_database_button_element.click()
    database_name_id = "database-name"
    ten_second_wait.until(
        method=expected_conditions.presence_of_element_located(
            locator=(By.ID, database_name_id),
        ),
    )

    database_name_element = driver.find_element(
        by=By.ID,
        value=database_name_id,
    )
    database_name_element.send_keys(database_name)

    cloud_type_radio_element = driver.find_element(
        by=By.ID,
        value="cloud-radio-btn",
    )
    cloud_type_radio_element.click()

    license_dropdown_element = Select(
        driver.find_element(
            by=By.ID,
            value="cloud-license-dropdown",
        ),
    )

    # Sleeping 1 second here did not work, so we sleep 5 seconds.
    time.sleep(5)
    license_dropdown_element.select_by_visible_text(text=license_name)

    create_button = driver.find_element(by=By.ID, value="create-btn")
    create_button.click()
    # Without this we might close the driver before the database is created.
    time.sleep(5)


@beartype
def get_database_details(
    driver: WebDriver,
    database_name: str,
) -> DatabaseDict:  # pragma: no cover
    """
    Get details of a database.
    """
    target_manager_url = "https://developer.vuforia.com/vui/develop/databases"
    driver.get(url=target_manager_url)
    ten_second_wait = WebDriverWait(driver=driver, timeout=10)

    ten_second_wait.until(
        expected_conditions.presence_of_element_located(
            (By.ID, "table_search"),
        ),
    )

    search_input_element = driver.find_element(by=By.ID, value="table_search")
    original_first_database_cell_element = ten_second_wait.until(
        expected_conditions.element_to_be_clickable(
            (By.ID, "table_row_0_project_name"),
        ),
    )
    search_input_element.send_keys(database_name)
    search_input_element.send_keys(Keys.RETURN)
    # The search has competed when the original first database cell element is
    # "stale".
    ten_second_wait.until(
        expected_conditions.staleness_of(original_first_database_cell_element),
    )

    # We assume that searching for the database name will return one result.
    database_cell_element = ten_second_wait.until(
        expected_conditions.element_to_be_clickable(
            (By.ID, "table_row_0_project_name"),
        ),
    )

    database_cell_element.click()

    access_keys_tab_item = ten_second_wait.until(
        expected_conditions.presence_of_element_located(
            (By.LINK_TEXT, "Database Access Keys"),
        ),
    )

    access_keys_tab_item.click()

    # Without this we sometimes get empty strings for the keys.
    time.sleep(1)

    client_access_key = driver.find_element(
        by=By.CLASS_NAME,
        value="client-access-key",
    ).text
    client_secret_key = driver.find_element(
        by=By.CLASS_NAME,
        value="client-secret-key",
    ).text
    server_access_key = driver.find_element(
        by=By.CLASS_NAME,
        value="server-access-key",
    ).text
    server_secret_key = driver.find_element(
        by=By.CLASS_NAME,
        value="server-secret-key",
    ).text

    return {
        "database_name": database_name,
        "server_access_key": str(server_access_key),
        "server_secret_key": str(server_secret_key),
        "client_access_key": str(client_access_key),
        "client_secret_key": str(client_secret_key),
    }


@click.group(name="vws-web")
@beartype
def vws_web_tools_group() -> None:
    """
    Commands for interacting with VWS.
    """


@click.command()
@click.option("--license-name", required=True)
@click.option("--email-address", envvar="VWS_EMAIL_ADDRESS", required=True)
@click.option("--password", envvar="VWS_PASSWORD", required=True)
@beartype
def create_vws_license(
    license_name: str,
    email_address: str,
    password: str,
) -> None:  # pragma: no cover
    """
    Create a license.
    """
    driver = webdriver.Safari()
    log_in(driver=driver, email_address=email_address, password=password)
    wait_for_logged_in(driver=driver)
    create_license(driver=driver, license_name=license_name)
    driver.close()


@click.command()
@click.option("--license-name", required=True)
@click.option("--database-name", required=True)
@click.option("--email-address", envvar="VWS_EMAIL_ADDRESS", required=True)
@click.option("--password", envvar="VWS_PASSWORD", required=True)
@beartype
def create_vws_database(
    database_name: str,
    license_name: str,
    email_address: str,
    password: str,
) -> None:  # pragma: no cover
    """
    Create a database.
    """
    driver = webdriver.Safari()
    log_in(driver=driver, email_address=email_address, password=password)
    wait_for_logged_in(driver=driver)
    create_database(
        driver=driver,
        database_name=database_name,
        license_name=license_name,
    )
    driver.close()


@click.command()
@click.option("--database-name", required=True)
@click.option("--email-address", envvar="VWS_EMAIL_ADDRESS", required=True)
@click.option("--password", envvar="VWS_PASSWORD", required=True)
@click.option("--env-var-format", is_flag=True)
@beartype
def show_database_details(
    database_name: str,
    email_address: str,
    password: str,
    *,
    env_var_format: bool,
) -> None:  # pragma: no cover
    """
    Show the details of a database.
    """
    driver = webdriver.Safari()
    log_in(driver=driver, email_address=email_address, password=password)
    wait_for_logged_in(driver=driver)
    details = get_database_details(driver=driver, database_name=database_name)
    driver.close()
    if env_var_format:
        env_var_format_details = {
            "VUFORIA_TARGET_MANAGER_DATABASE_NAME": details["database_name"],
            "VUFORIA_SERVER_ACCESS_KEY": details["server_access_key"],
            "VUFORIA_SERVER_SECRET_KEY": details["server_secret_key"],
            "VUFORIA_CLIENT_ACCESS_KEY": details["client_access_key"],
            "VUFORIA_CLIENT_SECRET_KEY": details["client_secret_key"],
        }

        for key, value in env_var_format_details.items():
            click.echo(message=f"{key}={value}")
    else:
        click.echo(message=yaml.dump(data=details), nl=False)


vws_web_tools_group.add_command(create_vws_database)
vws_web_tools_group.add_command(create_vws_license)
vws_web_tools_group.add_command(show_database_details)
