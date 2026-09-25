package auth

import (
	"strconv"
	"testing"
)

func TestJWTGenerateAndValidate(t *testing.T) {
	kunciRahasia := "kunci_rahasia_tes_123456"
	idPengguna := int64(42)
	peran := PeranAdmin

	stringToken, detikKedaluwarsa, galat := BuatToken(idPengguna, peran, kunciRahasia, 24)
	if galat != nil {
		t.Fatalf("diharapkan tidak ada galat saat membuat token, diterima: %v", galat)
	}

	if stringToken == "" {
		t.Fatal("diharapkan token tidak kosong")
	}

	if detikKedaluwarsa != 86400 {
		t.Fatalf("diharapkan 86400 detik, diterima: %d", detikKedaluwarsa)
	}

	// Validasi token yang sah
	klaim, galat := ValidasiToken(stringToken, kunciRahasia)
	if galat != nil {
		t.Fatalf("diharapkan validasi token berhasil, diterima: %v", galat)
	}

	if klaim.Peran != peran {
		t.Fatalf("diharapkan peran %s, diterima: %s", peran, klaim.Peran)
	}

	if klaim.Subject != strconv.FormatInt(idPengguna, 10) {
		t.Fatalf("diharapkan subjek %d, diterima: %s", idPengguna, klaim.Subject)
	}

	// Validasi token dengan rahasia salah
	_, galat = ValidasiToken(stringToken, "kunci_rahasia_salah")
	if galat == nil {
		t.Fatal("diharapkan galat validasi dengan rahasia yang salah, diterima nil")
	}
}
