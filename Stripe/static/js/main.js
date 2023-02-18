console.log("Sanity check!");

var stripe = Stripe("{{ STRIPE_PUBLIC_KEY }}");
var checkoutButton = document.getElementById("checkout-button").addEventListener("click", function () {
  fetch('/buy/2/', {
    method: "GET",

  })
    .then(function (response) {
      return response.json();
    })
    .then(function (session) {
      return stripe.redirectToCheckout({ sessionId: session.id });
    })
  });
