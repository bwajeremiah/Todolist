<script setup>
import { ref } from 'vue'
const notesData = ref([])
const errorMessage = ref('')
const newNoteText = ref('')
const selectDelete = ref('')
async function fetchNotes() {
  errorMessage.value = ''

  try {
    const response = await fetch('/api/notes/')
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`)
    }

    notesData.value = await response.json()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Unable to fetch notes'
  }
}
async function addNote() {
  errorMessage.value = ""
  try {
    const response = await fetch('/api/notes', {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text: newNoteText.value })
    })
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`)
    }

    notesData.value = await response.json()
    newNoteText.value = ''
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Unable to add note'
  }
}
async function addAndShowNote() {
  await addNote()
  await fetchNotes()
}
async function deleteNote(id) {
  errorMessage.value = ''
  try {
    const response = await fetch(`/api/notes/${id}`, {
      method: 'DELETE'
    })
    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`)
    }
    await fetchNotes()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Unable to delete note'
  }
}
</script>

<template>
  <button @click="fetchNotes">Fetch Notes</button>
  <p v-if="errorMessage">{{ errorMessage }}</p>
  <ul v-else-if="notesData.length">
    <li v-for="note in notesData" :key="note.id">
      {{ note.text }} (ID: {{ note.id }}, last edited: {{ note.last_edited_date }})
    </li>
  </ul>
  <p v-else>No notes loaded yet.</p>
  <input v-model="newNoteText" placeholder="Enter a new note"></input>
  <button @click="addAndShowNote">Add Note</button>
  <input v-model="selectDelete" placeholder="Enter the ID of the note to delete">
  <button @click="deleteNote(selectDelete)">Delete</button>
</template>