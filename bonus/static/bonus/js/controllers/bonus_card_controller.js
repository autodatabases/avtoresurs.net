/**
 * Created by shaman on 5/25/17.
 */
bonusApp.controller('BonusCardController',
    function ($scope) {
        var bonusModal = $('#bonus-modal');
        var modalTitle = $('#bonus-title');
        var modalPrice = $('#bonus-price');
        var title = '';
        var price = '';

        $scope.BonusCardClick = function ($title, $price) {
            title = $title;
            price = $price;
            bonusModal.modal('open');
            modalTitle.html(title);
            modalPrice.html(price);
        };

        $scope.GetBonusClick = function () {
            alert("get bonus click angular event");
        };
    }
);
