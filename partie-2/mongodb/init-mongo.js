// Se connecte à MongoDB et créé la base de données "test" si elle n'existe pas
db = db.getSiblingDB("test"); 

if (!db.getCollectionNames().includes("users")) {
    db.createCollection("users"); // Créer la collection si elle n'existe pas

    // Insére des utilisateurs par défaut
    db.users.insertMany([
        {
            username: "admin",
            password: "admin", 
            role: "ADMIN"
        },
        {
            username: "user",
            password: "user",
            role: "USER"
        }
    ]);

    print("Base de données et utilisateurs initialisés !");
} else {
    print("La base 'test' et la collection 'users' existent déjà.");
}
