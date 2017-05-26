/**
 * Created by shaman on 5/25/17.
 */
bonusApp.controller('BonusCardController',
    function ($scope, $http) {
        var bonusModal = $('#bonus-modal');
        var modalTitle = $('#bonus-title');
        var modalPrice = $('#bonus-price');
        var preloader = $('#preloader');
        var getBtn = $('#get-btn');
        var cancelBtn = $('#cancel-btn');
        var title = '';
        var price = '';
        var bonus_id = null;
        var user_id = null;
        var protected_key = 'GsdfklGsdn6305cHdshy';

        $scope.BonusCardClick = function ($title, $price, $points, $bonus_id, $user_id) {
            title = $title;
            price = $price;
            bonus_id = $bonus_id;
            user_id = $user_id;
            getBtn.show();
            preloader.hide();
            cancelBtn.show();
            bonusModal.modal('open');
            modalTitle.html(title);
            modalPrice.html("Необходимо " + $price + " баллов. <br/> Ваши баллы: " + $points);
        };

        $scope.GetBonusClick = function ($points) {
            if (parseInt(price) < parseInt($points)) {
                var url = '/bonus/obtain/?bonus_id=' + bonus_id;
                preloader.show();
                $http.post(url, {id: user_id, key: protected_key})
                .then(function(response) {
                    modalPrice.html(response.data);
                    getBtn.hide();
                    cancelBtn.hide();
                    preloader.hide();
                    setTimeout(window.location='/bonus/', 700);
                });
            } else {
                modalPrice.html("Необходимо " + price + " баллов. <br/> Ваши баллы: " + $points + "<br/><span style='color: darkred;'>Вам не хватает баллов!</span>");
            }
        };
    }
);
