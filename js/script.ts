interface Plat {
  nom: string;
  prix: number;
  categorie: string;
}

// ---------- 1. Menu "hamburger" ----------
const boutonMenu = document.querySelector<HTMLButtonElement>("#bouton-menu");
const nav = document.querySelector<HTMLElement>("nav");

if (boutonMenu && nav) {
  boutonMenu.addEventListener("click", () => {
    nav.classList.toggle("ouvert");
  });
}

// ---------- 2. Vérification du formulaire de réservation ----------
const form = document.querySelector<HTMLFormElement>("#form-reservation");

if (form) {
  const erreur = document.querySelector<HTMLElement>("#erreur");
  const champNom = form.querySelector<HTMLInputElement>("#nom")!;
  const champTel = form.querySelector<HTMLInputElement>("#telephone")!;
  const champDate = form.querySelector<HTMLInputElement>("#date")!;
  const champPersonnes = form.querySelector<HTMLInputElement>("#personnes")!;

  form.addEventListener("submit", (evenement: Event) => {
    const messages: string[] = [];
    const tel: string = champTel.value.replace(/\s/g, "");
    const personnes: number = Number(champPersonnes.value);
    const jour: Date = new Date(champDate.value);
    const aujourdhui: Date = new Date();
    aujourdhui.setHours(0, 0, 0, 0);

    if (champNom.value.trim() === "") messages.push("Indiquez votre nom.");
    if (!/^6\d{8}$/.test(tel)) messages.push("Numéro invalide : 9 chiffres commençant par 6.");
    if (!(personnes >= 1 && personnes <= 20)) messages.push("Entre 1 et 20 personnes.");
    if (isNaN(jour.getTime()) || jour < aujourdhui) messages.push("Choisissez une date à venir.");

    if (messages.length > 0) {
      evenement.preventDefault();
      if (erreur) erreur.textContent = messages.join(" ");
    }
  });
}

// ---------- 3. Menu chargé depuis un fichier JSON, avec filtre ----------
const liste = document.querySelector<HTMLUListElement>("#liste-menu");
let tousLesPlats: Plat[] = [];

function afficherPlats(conteneur: HTMLElement, categorie: string): void {
  conteneur.textContent = "";
  const plats: Plat[] = categorie === "tout"
    ? tousLesPlats
    : tousLesPlats.filter((p) => p.categorie === categorie);

  for (const p of plats) {
    const li = document.createElement("li");
    li.textContent = `${p.nom} : ${p.prix} FCFA`;
    conteneur.appendChild(li);
  }
}

async function chargerMenu(conteneur: HTMLElement): Promise<void> {
  try {
    const reponse = await fetch("menu.json");
    if (!reponse.ok) throw new Error("Erreur " + reponse.status);
    tousLesPlats = (await reponse.json()) as Plat[];
    afficherPlats(conteneur, "tout");
  } catch (e) {
    conteneur.textContent = "Le menu est momentanément indisponible.";
    console.error(e);
  }
}

if (liste) {
  chargerMenu(liste);
  document.querySelectorAll<HTMLButtonElement>(".filtre").forEach((bouton) => {
    bouton.addEventListener("click", () => {
      afficherPlats(liste, bouton.dataset.categorie ?? "tout");
    });
  });
}