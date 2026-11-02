<script setup>
import { ref } from 'vue'
const notesData = ref(null)
 async function fetchNotes() {
  const response = await fetch('/api/notes');
  const data = await response.json();
  notesData.value = data;
  console.log(notesData.value);
}
</script>

<template>
  <button @click="fetchNotes">Fetch Notes</button>
    <p>{{ notesData }}</p>
</template>