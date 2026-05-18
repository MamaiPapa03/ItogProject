# ItogProject
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>База фильмов</title>
</head>
<body>
    <div class="container">
        <h1>Добавление фильма</h1>
        
        <form id="movieForm">
            <div>
                <label for="title">Название:</label>
                <input type="text" id="title" required>
            </div>
            <div>
                <label for="genre">Жанр:</label>
                <input type="text" id="genre" required>
            </div>
            <div>
                <label for="year">Год выпуска:</label>
                <input type="number" id="year" required>
            </div>
            <div>
                <label for="rating">Рейтинг (0–10):</label>
                <input type="number" id="rating" min="0" max="10" step="0.1" required>
            </div>
            <button type="submit">Добавить фильм</button>
        </form>

        <div class="filters">
            <label for="filterGenre">Фильтр по жанру:</label>
            <input type="text" id="filterGenre">
            
            <label for="filterYear">Фильтр по году:</label>
            <input type="number" id="filterYear">
            <button id="applyFilters">Применить фильтры</button>
            <button id="clearFilters">Сбросить фильтры</button>
        </div>

        <table id="moviesTable">
            <thead>
                <tr>
                    <th>Название</th>
                    <th>Жанр</th>
                    <th>Год выпуска</th>
                    <th>Рейтинг</th>
                </tr>
            </thead>
            <tbody id="tableBody">
                <!-- Сюда будут добавляться строки с фильмами -->
            </tbody>
        </table>
    </div>

    <script src="script.js"></script>
</body>
</html>
