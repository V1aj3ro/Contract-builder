<template>
  <nav>
    <RouterLink to="/">Договоры</RouterLink>
    |
    <RouterLink to="/customers">Заказчики</RouterLink>
    |
    <RouterLink to="/disciplines">Дисциплины</RouterLink>
    |
    <RouterLink to="/contracts/new">Новый договор</RouterLink>
  </nav>
  <RouterView />
</template>