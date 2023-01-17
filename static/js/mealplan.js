// Allow a user to drag recipes to the MealPlan container to add them to the MealPlan
// When a recipe is dragged and dropped, an ajax request is sent to add that recipe to that day's mealplan

const mealPlanContainer = document.querySelector('#meal-plan')
const recipesContainer = document.querySelector('#recipes')
const addRemoveRecipeURL = recipesContainer.dataset.addRemoveUrl
const mealPlanDate = moment(new Date(mealPlanContainer.dataset.date)).format(
  'YYYY-MM-DD'
)

dragula([recipesContainer, mealPlanContainer]).on('drop', (el) => {
  const data = new FormData()
  data.append('date', mealPlanDate)
  data.append('pk', el.dataset.pk)

  fetch(addRemoveRecipeURL, {
    method: 'POST',
    headers: { 'X-Requested-With': 'XMLHttpRequest' },
    body: data,
  })
    .then((res) => res.json())
    .then((data) => console.log('got here'))
    .catch((error) => console.log(error))
})
