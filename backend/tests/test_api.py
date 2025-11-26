"""
Tests API TaskFlow - Atelier 1 Starter

Apprenez en faisant ! Ce fichier vous montre comment écrire des tests, puis vous en écrirez de similaires.

Structure de chaque test :
1. ARRANGE - Préparer les données de test
2. ACT - Faire la requête API
3. ASSERT - Vérifier la réponse
"""

import pytest


# =============================================================================
# PARTIE 1 : TESTS EXEMPLES (Apprenez de ceux-ci !)
# =============================================================================

def test_root_endpoint(client):
    """
    EXEMPLE : Tester un point de terminaison GET simple.

    Ce test vous montre le pattern de base :
    1. Faire une requête avec client.get()
    2. Vérifier le code de statut
    3. Vérifier les données de la réponse
    """
    # ACT : Faire une requête GET
    response = client.get("/")

    # ASSERT : Vérifier la réponse
    assert response.status_code == 200
    assert "Welcome to TaskFlow API" in response.json()["message"]


def test_health_check(client):
    """EXEMPLE : Un autre test de point de terminaison GET simple."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task(client):
    """
    EXEMPLE : Tester un point de terminaison POST (création de données).

    Pattern pour les requêtes POST :
    1. Préparer les données comme un dictionnaire Python
    2. Les envoyer avec client.post()
    3. Vérifier le code de statut (201 = Créé)
    4. Vérifier les données retournées
    """
    # ARRANGE : Préparer les données
    new_task = {
        "title": "Acheter des courses",
        "description": "Lait, œufs, pain"
    }

    # ACT : Envoyer la requête POST
    response = client.post("/tasks", json=new_task)

    # ASSERT : Vérifier la réponse
    assert response.status_code == 201  # 201 = Créé

    task = response.json()
    assert task["title"] == "Acheter des courses"
    assert task["description"] == "Lait, œufs, pain"
    assert task["status"] == "todo"  # Valeur par défaut
    assert "id" in task  # Le serveur génère un ID


def test_list_tasks(client):
    """
    EXEMPLE : Tester GET avec préparation de données.

    Parfois vous devez créer des données d'abord, puis tester leur listage.
    """
    # ARRANGE : Créer quelques tâches d'abord
    client.post("/tasks", json={"title": "Tâche 1"})
    client.post("/tasks", json={"title": "Tâche 2"})

    # ACT : Obtenir la liste des tâches
    response = client.get("/tasks")

    # ASSERT : Vérifier qu'on a bien les deux tâches
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_get_task_by_id(client):
    """
    EXEMPLE : Tester GET pour une ressource spécifique.

    Pattern :
    1. Créer une tâche d'abord
    2. Obtenir son ID depuis la réponse
    3. Utiliser cet ID pour récupérer la tâche
    """
    # ARRANGE : Créer une tâche
    create_response = client.post("/tasks", json={"title": "Trouve-moi"})
    task_id = create_response.json()["id"]

    # ACT : Obtenir la tâche spécifique
    response = client.get(f"/tasks/{task_id}")

    # ASSERT : Vérifier qu'on a la bonne tâche
    assert response.status_code == 200
    assert response.json()["title"] == "Trouve-moi"


# =============================================================================
# PARTIE 2 : À VOUS ! Complétez ces tests
# =============================================================================

# EXERCICE 1 : Écrire un test pour SUPPRIMER une tâche
# Pattern : Créer → Supprimer → Vérifier qu'elle a disparu
def test_delete_task(client):
    """
    VOTRE TÂCHE : Écrire un test qui supprime une tâche.

    Étapes :
    1. Créer une tâche (comme dans test_create_task)
    2. Obtenir son ID
    3. Envoyer une requête DELETE : client.delete(f"/tasks/{task_id}")
    4. Vérifier que le code de statut est 204 (No Content)
    5. Essayer de GET la tâche à nouveau → devrait retourner 404 (Not Found)

    Astuce : Regardez test_get_task_by_id pour voir comment créer et obtenir l'ID
    """
    # TODO : Écrivez votre test ici !
    new_task = {
        "title": "Acheter des courses",
        "description": "Lait, œufs, pain"
    }
    create_resp = client.post("/tasks", json=new_task)
    assert create_resp.status_code == 201
    created = create_resp.json()

    # 2) Récupérer son ID (id ou task_id selon votre API)
    task_id = created.get("id", created.get("task_id"))
    assert task_id is not None, f"Réponse de création inattendue: {created}"

    # 3) Supprimer la tâche
    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 204

    # 4) Vérifier qu’elle n’existe plus
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404

def test_delete_nonexistent_task_returns_404(client):
    """Deleting a task that doesn't exist should return 404."""
    test_task_id = 9999

    # 1) Essayer de supprimer une tâche inexistante
    resp = client.delete(f"/tasks/{test_task_id}")

    # 2) Doit retourner 404
    assert resp.status_code == 404

    # 3) Le message d'erreur contient "not found"
    detail = (resp.json().get("detail") or "")
    assert "not found" in detail.lower()


# EXERCICE 2 : Écrire un test pour METTRE À JOUR une tâche
# Pattern : Créer → Mettre à jour → Vérifier les changements
def test_update_task(client):
    """
    VOTRE TÂCHE : Écrire un test qui met à jour le titre d'une tâche.

    Étapes :
    1. Créer une tâche avec le titre "Titre Original"
    2. Obtenir son ID
    3. Envoyer une requête PUT : client.put(f"/tasks/{task_id}", json={"title": "Nouveau Titre"})
    4. Vérifier que le code de statut est 200
    5. Vérifier que la réponse contient le nouveau titre

    Astuce : Les requêtes PUT sont comme les POST, mais elles modifient des données existantes
    """
    create_response = client.post("/tasks", json={"title": "Trouve-moi"})
    task_id = create_response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"title": "Nouveau Titre" })

    assert response.status_code == 200

    assert response.json()["title"] == "Nouveau Titre"


# EXERCICE 3 : Tester la validation - un titre vide devrait échouer
def test_create_task_empty_title(client):
    """
    VOTRE TÂCHE : Tester que créer une tâche avec un titre vide échoue.

    Étapes :
    1. Essayer de créer une tâche avec title = ""
    2. Vérifier que le code de statut est 422 (Erreur de Validation)

    Astuce : Regardez test_create_task, mais attendez-vous à un échec !
    """
    # TODO : Écrivez votre test ici !
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 422

def test_health_check(client):
response = client.get("/health")
assert response.status_code == 200
assert response.json()["status"] == "BROKEN" # ❌ Faux exprès !




# EXERCICE 4 : Tester la validation - priorité invalide
def test_update_task_with_invalid_priority(client):
    """
    VOTRE TÂCHE : Tester qu'on ne peut pas mettre à jour une tâche avec une priorité invalide.

    Étapes :
    1. Créer une tâche valide
    2. Essayer de la mettre à jour avec priority="urgent" (invalide)
    3. Vérifier que le code de statut est 422 (Erreur de Validation)

    Rappel : Les priorités valides sont "low", "medium", "high" (voir TaskPriority dans app.py)
    """
    create_response = client.post("/tasks", json={"title": "Trouve-moi"})
    task_id = create_response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"title": "Nouveau Titre", "priority": "urgent" })

    assert response.status_code == 422


# EXERCICE 5 : Tester l'erreur 404
def test_get_nonexistent_task(client):
    """
    Obtenir une tâche qui n'existe pas doit retourner 404.
    """
    fake_id = 999  # ou 10_000_000 pour éviter toute collision

    resp = client.get(f"/tasks/{fake_id}")

    # 1) Statut 404
    assert resp.status_code == 404

    # 2) Message d'erreur (optionnel mais utile)
    detail = (resp.json().get("detail") or "")
    assert "not found" in detail.lower()

def test_filter_by_multiple_criteria(client):
    """Filtering by status AND priority should work."""
    def create_task(title, status, priority):
        resp = client.post(
            "/tasks",
            json={
                "title": title,
                "status": status,      # ex: "todo" | "in_progress" | "done"
                "priority": priority,  # ex: "low" | "medium" | "high"
            },
        )
        assert resp.status_code in (200, 201)
        body = resp.json()
        assert "id" in body
        return body["id"]

    # 1) Créer 3 tâches avec différents status et priority
    t1_id = create_task("T1", status="todo", priority="high")   # doit correspondre
    create_task("T2", status="todo", priority="low")            # écartée par priority
    create_task("T3", status="done", priority="high")           # écartée par status

    # 2) Filtrer: status=todo & priority=high
    resp = client.get("/tasks", params={"status": "todo", "priority": "high"})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

    # 3) Vérifier qu'on reçoit seulement les bonnes tâches
    returned_ids = {item.get("id") for item in data}
    assert returned_ids == {t1_id}, f"Expected only task {t1_id}, got {returned_ids}"

    # (Garde-fous supplémentaires)
    for item in data:
        assert item.get("status") == "todo"
        assert item.get("priority") == "high"


# =============================================================================
# EXERCICES BONUS (Si vous finissez en avance !)
# =============================================================================

# BONUS 1 : Tester le filtrage par statut
def test_filter_tasks_by_status(client):
    """
    BONUS : Tester le filtrage des tâches par statut.

    Étapes :
    1. Créer 2 tâches : une avec status="todo", une avec status="done"
    2. Obtenir les tâches avec le filtre : client.get("/tasks?status=done")
    3. Vérifier que seule la tâche "done" est retournée
    """
    # TODO : Écrivez votre test ici !
    pass


# BONUS 2 : Tester la mise à jour d'un seul champ
def test_update_only_status(client):
    """
    BONUS : Tester que mettre à jour seulement le statut ne change pas les autres champs.

    Étapes :
    1. Créer une tâche avec title="Test" et status="todo"
    2. Mettre à jour seulement le statut à "done"
    3. Vérifier que le statut a changé MAIS le titre est resté le même
    """
    # TODO : Écrivez votre test ici !
    pass


# BONUS 3 : Tester le cycle de vie complet d'une tâche
def test_task_lifecycle(client):
    """
    BONUS : Tester le cycle de vie complet : Créer → Lire → Mettre à jour → Supprimer

    Étapes :
    1. Créer une tâche
    2. La lire (GET par ID)
    3. La mettre à jour (changer le statut à "done")
    4. La supprimer
    5. Vérifier qu'elle a disparu (GET devrait retourner 404)
    """
    # TODO : Écrivez votre test ici !
    pass


# =============================================================================
# ASTUCES & CONSEILS
# =============================================================================

"""
PATTERNS COURANTS :

1. Tester POST (Créer) :
   response = client.post("/tasks", json={"title": "..."})
   assert response.status_code == 201

2. Tester GET (Lire) :
   response = client.get("/tasks")
   assert response.status_code == 200

3. Tester PUT (Mettre à jour) :
   response = client.put(f"/tasks/{id}", json={"title": "..."})
   assert response.status_code == 200

4. Tester DELETE (Supprimer) :
   response = client.delete(f"/tasks/{id}")
   assert response.status_code == 204

5. Tester les erreurs de validation :
   response = client.post("/tasks", json={"bad": "data"})
   assert response.status_code == 422

6. Tester les erreurs 404 :
   response = client.get("/tasks/999")
   assert response.status_code == 404

CODES DE STATUT COURANTS :
- 200 : OK (GET/PUT réussi)
- 201 : Créé (POST réussi)
- 204 : Pas de Contenu (DELETE réussi)
- 404 : Non Trouvé (la ressource n'existe pas)
- 422 : Erreur de Validation (données invalides)

RAPPELEZ-VOUS :
- La fixture `client` est automatiquement fournie par conftest.py
- La base de données est automatiquement nettoyée avant/après chaque test
- Les tests doivent être indépendants (ne pas dépendre d'autres tests)
"""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
