<template>
  <header class="container">
    <nav>
      <ul>
        <li><strong>Contract Builder</strong></li>
      </ul>
      <ul>
        <li><RouterLink to="/">Договоры</RouterLink></li>
        <li><RouterLink to="/contractors">Исполнители</RouterLink></li>
        <li><RouterLink to="/customers">Заказчики</RouterLink></li>
        <li><RouterLink to="/disciplines">Дисциплины</RouterLink></li>
        <li><RouterLink to="/contracts/new"><strong>+ Новый договор</strong></RouterLink></li>
      </ul>
    </nav>
  </header>
  <main class="container">
    <RouterView />
  </main>
</template>