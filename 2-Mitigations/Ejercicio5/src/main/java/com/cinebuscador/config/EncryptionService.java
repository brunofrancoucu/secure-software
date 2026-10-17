package com.cinebuscador.config;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

/**
 * Servicio para contraseñas.
 */
public class EncryptionService {
    // Instanciamos el encoder de BCrypt con fuerza 10 (por defecto)
    private static final BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();

    /**
     * Genera un hash con un salt aleatorio.
     */
    public static String hashPassword(String rawPassword) {
        return encoder.encode(rawPassword);
    }

    /**
     * Compara una contraseña en texto plano contra el hash almacenado en la base de datos.
     */
    public static boolean checkPassword(String rawPassword, String hashedPassword) {
        return encoder.matches(rawPassword, hashedPassword);
    }
}
