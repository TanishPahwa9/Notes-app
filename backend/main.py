from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Notes API")

notes = []   # abhi data yahin rahega, server band to data gaya
next_id = 1


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str | None = None


@app.get("/notes")
def list_notes():
    return notes


@app.post("/notes", status_code=201)
def create_note(note: NoteIn):
    global next_id
    item = {"id": next_id, **note.model_dump()}
    notes.append(item)
    next_id += 1
    return item


@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for n in notes:
        if n["id"] == note_id:
            notes.remove(n)
            return {"deleted": note_id}
    raise HTTPException(status_code=404, detail="Note not found")