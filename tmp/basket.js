/* Реализовать модуль корзины. Создать блок товаров и блок корзины. 
У каждого товара есть кнопка «Купить», при нажатии на которую происходит добавление имени и цены товара в блок корзины.
Корзина должна уметь считать общую сумму заказа. */


function main(){
    // инициализируем объекты в виде атрибутов window 
    // для глобального доступа к их интерфесам
    window.catalog = new TableRenderer('catalog', catalogData);
    window.cart = new CartRenderer('cart');
}

class TableRenderer{
    constructor(tableType, data){
        this.tableType = tableType;
        this.containerObject = document.getElementById(tableType);
        this.content = [];
        this.tableBuilt = false;
        if (data){
            this.content = data;
            this.initTable();
            this.fillTable();
        }
    }
    initTable(){
        // удаляем из верстки сообщение "каталог/корзина пуста"
        if (document.getElementById(`${this.tableType}-empty-message`)){
            document.getElementById(`${this.tableType}-empty-message`).remove();
        }
        // у каталога в шапке рядом с количеством будет примечание "в наличии"
        let quantityHeader = (this.tableType === 'catalog') ? 'Количество(в наличии)' : 'Количество';
        // отрисовываем шапку таблицы
        this.containerObject.insertAdjacentHTML('afterbegin', 
                                                `<div class="table-responsive">
                                                    <table class="table text-center">
                                                        <thead>
                                                            <tr>
                                                                <th>Название</th>                
                                                                <th>Цена</th>    
                                                                <th>${quantityHeader}</th>
                                                                <th>Кнопка</th>                                        
                                                            </tr>
                                                        </thead>
                                                        <tbody id="${this.tableType}-list"></tbody>
                                                    </table>
                                                </div>`)
        // возвращаем тело таблицы(tableObject) 
        this.tableObject = document.getElementById(`${this.tableType}-list`);
        this.tableBuilt = true;
    }
    fillTable(){
        // перебираем данные о товарах и передаем значения атрибутов
        // каждого товара в виде аргумента вспомогательной функции renderRow
        for (let item of this.content){
            this.renderRow(item.id, item.title, item.price, item.quantity);
        }
    }
    renderRow(id, title, price, quantity){
        // в зависимости от вида таблицы будет отличаться кнопка - купить/удалить
        // и префикс id узла таблицы
        if (this.tableType === 'catalog'){
            this.button = '<td><button onclick="addProduct(event)" type="button" class="btn btn-success">Купить</button></td>' 
        } else {
            this.button = '<td><button onclick="removeProduct(event)" type="button" class="btn btn-danger">Удалить</button></td>' 
        }
        // вставляем элемент в конец таблицы с переданными параметрами
        // id не отображаем, а передаем как id узла ряда таблицы с префиксом "catalog-" / "cart-"
        this.tableObject.insertAdjacentHTML('beforeend', 
                                                `<tr id="${this.tableType}-${id}">
                                                    <th scope="row" class="text-start">${title}</th>    
                                                    <td>${price}</td>
                                                    <td>${quantity}</td>
                                                    ${this.button}                                    
                                                </tr>`);
    }
}

class CartRenderer extends TableRenderer {
    addCartInfo(){
        if(document.getElementById('cart-info')) {
            document.getElementById('cart-info').remove();
        }
        this.totalQuantity = 0; 
        this.totalPrice = 0;
        for (let item of this.content){
            this.totalQuantity += item.quantity;
            this.totalPrice += item.price * item.quantity;
        };
        this.containerObject.insertAdjacentHTML('beforeend', 
                                            `<p id="cart-info">
                                                В корзине: ${this.totalQuantity} товаров на сумму ${this.totalPrice} рублей
                                            </p>`)
    }
    addProduct(productId){
        let productObject = this.content.find((item, index) => {
            if(item.id == productId) return true;
        });
        // в корзине есть такой товар - увеличиваем на 1
        if (productObject) {
            productObject.quantity += 1;
            // товар в корзине был
            return true
        } else {
            // в корзине такого товара нет - находим товар в каталоге, 
            // добавляем его с количеством 1
            let productCatalogObject = window.catalog.content.find((item, index) => {
                if(item.id == productId) return true;
            });
            window.cart.content.push({
                id: productCatalogObject.id,
                title: productCatalogObject.title,
                price: productCatalogObject.price,
                quantity: 1
            });
            // товара в корзине не было
            return false;
        }
    }
    removeProduct(productId){
        // обновляем цифру в объекте корзины
        let productObject = window.cart.content.find((item, index) => {
            if(item.id == productId) return true;
        });
        productObject.quantity -= 1;
        if (productObject.quantity == 0){
            let index = this.content.findIndex(item => {
                if(item.id == productId) return true;
            });
            this.content.splice(index, 1);
            return false;
        }
        return true;
    }
}

function addProduct(event){
    // находим id и обновляем цифру в объекте корзины
    let productId = event.target.parentNode.parentNode.id.split('-')[1];
    // метод корзины вернет true если товар в уже был
    // первый случай: товар есть в корзине
    if (window.cart.addProduct(productId)){
        // обновляем цифру на странице 
        let productTableRow = document.getElementById(`cart-${productId}`);
        let price = productTableRow.childNodes[5];
        // обновляем отображение на странице
        newValue = Number(price.innerText) + 1;
        price.innerText = String(newValue);
    // второй случай: в таблице еще нет других товаров
    } else {
        // отрисовываем корзину если не отрисована
        if (!window.cart.tableBuilt) window.cart.initTable();
        // отрисовываем товар в корзине
        let productObject = window.cart.content.find((item, index) => {
            if(item.id == productId) return true;
        })
        window.cart.renderRow(productObject.id, productObject.title, productObject.price, 1)
    }
    window.cart.addCartInfo();
}

function removeProduct(event){
    let productId = event.target.parentNode.parentNode.id.split('-')[1];
    let quantityNode = event.target.parentNode.previousSibling.previousSibling;
    // первый случай: в таблице больше одного товара который мы пытаемся удалить
    if (window.cart.removeProduct(productId)){
        // обновляем цифру на странице 
        quantityNode.innerText = String(Number(quantityNode.innerText) - 1);
        // выводим комментарий с информацией о корзине
        window.cart.addCartInfo();
    // второй случай: в корзине товар последний
    } else {
        // удаляем узел/ряд товара из корзины
        quantityNode.parentNode.remove();
        // делаем проверку что мы не удалили последний элемент из таблицы
        if (window.cart.tableObject.childElementCount == 0){
            // очищаем контейнер корзины
            while(window.cart.containerObject.firstChild){
                window.cart.containerObject.removeChild(window.cart.containerObject.firstChild);
            } 
            // добавляем сообщение "корзина пуста"
            window.cart.containerObject.insertAdjacentHTML('afterbegin', '<p id="cart-empty-message" class="text-center">Корзина пуста...</p>');
            // меняем флаг на ложь
            window.cart.tableBuilt = false;
        } else {
            window.cart.addCartInfo();
        }
    }
}

main()
