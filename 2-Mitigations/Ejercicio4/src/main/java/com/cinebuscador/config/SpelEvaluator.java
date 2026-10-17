package com.cinebuscador.config;

import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.SimpleEvaluationContext;
import org.springframework.expression.spel.support.StandardEvaluationContext;
import org.springframework.stereotype.Component;


@Component
public class SpelEvaluator {


    public String evaluate(String expression) {
        if (expression == null || expression.isBlank()) {
            return "";
        }

        ExpressionParser parser = new SpelExpressionParser();
        
        // Instanciar solo lectura
        
        org.springframework.expression.EvaluationContext context =
            SimpleEvaluationContext.forReadOnlyDataBinding().build();

        try {
            var expr = parser.parseExpression(expression);
            Object result = expr.getValue(context);
            return result != null ? result.toString() : "";
        } catch (Exception e) {
            return "Error en la búsqueda";
        }
    }
}
