import allure


class AssertHelper:
    @staticmethod
    @allure.step("Сравниваем объявления")
    def assert_ads(actual_ads, expected_ads):
        assert actual_ads["id"] == expected_ads["id"]
        assert actual_ads["name"] == expected_ads["name"]
        assert actual_ads["condition"] == expected_ads["condition"]
        assert actual_ads["category"] == expected_ads["category"]
        assert actual_ads["city"] == expected_ads["city"]
        assert actual_ads["description"] == expected_ads["description"]
        assert str(actual_ads["price"]) == str(expected_ads["price"])