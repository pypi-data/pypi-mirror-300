use crate::{
    compiler,
    error::{error, no_error, ErrorIterator, ValidationError},
    keywords::{helpers::fail_on_non_positive_integer, CompilationResult},
    paths::{JsonPointer, JsonPointerNode},
    validator::Validate,
};
use serde_json::{Map, Value};

pub(crate) struct MinItemsValidator {
    limit: u64,
    schema_path: JsonPointer,
}

impl MinItemsValidator {
    #[inline]
    pub(crate) fn compile<'a>(
        ctx: &compiler::Context,
        schema: &'a Value,
        schema_path: JsonPointer,
    ) -> CompilationResult<'a> {
        if let Some(limit) = schema.as_u64() {
            return Ok(Box::new(MinItemsValidator { limit, schema_path }));
        }
        if ctx.supports_integer_valued_numbers() {
            if let Some(limit) = schema.as_f64() {
                if limit.trunc() == limit {
                    #[allow(clippy::cast_possible_truncation)]
                    return Ok(Box::new(MinItemsValidator {
                        // NOTE: Imprecise cast as big integers are not supported yet
                        limit: limit as u64,
                        schema_path,
                    }));
                }
            }
        }
        Err(fail_on_non_positive_integer(schema, schema_path))
    }
}

impl Validate for MinItemsValidator {
    fn is_valid(&self, instance: &Value) -> bool {
        if let Value::Array(items) = instance {
            if (items.len() as u64) < self.limit {
                return false;
            }
        }
        true
    }

    fn validate<'instance>(
        &self,
        instance: &'instance Value,
        instance_path: &JsonPointerNode,
    ) -> ErrorIterator<'instance> {
        if let Value::Array(items) = instance {
            if (items.len() as u64) < self.limit {
                return error(ValidationError::min_items(
                    self.schema_path.clone(),
                    instance_path.into(),
                    instance,
                    self.limit,
                ));
            }
        }
        no_error()
    }
}

#[inline]
pub(crate) fn compile<'a>(
    ctx: &compiler::Context,
    _: &'a Map<String, Value>,
    schema: &'a Value,
) -> Option<CompilationResult<'a>> {
    let schema_path = ctx.as_pointer_with("minItems");
    Some(MinItemsValidator::compile(ctx, schema, schema_path))
}

#[cfg(test)]
mod tests {
    use crate::tests_util;
    use serde_json::json;

    #[test]
    fn schema_path() {
        tests_util::assert_schema_path(&json!({"minItems": 1}), &json!([]), "/minItems")
    }
}
