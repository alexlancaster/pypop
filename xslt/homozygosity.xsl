<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <!-- ################  HOMOZYGOSITY STATISTICS ###################### --> 
 
 <xsl:template match="homozygosity">
  <xsl:call-template name="section">
   <xsl:with-param name="title">
    <xsl:call-template name="locus-header">
     <xsl:with-param name="title">
      <xsl:text>Ewens-Watterson homozygosity test of neutrality</xsl:text>
     </xsl:with-param>
    </xsl:call-template>
   </xsl:with-param>
   <xsl:with-param name="level" select="3"/>
   <xsl:with-param name="text">

    <xsl:choose>

     <xsl:when test="@role='out-of-range'">
      <xsl:text>*Out of range of simulated homozygosity values*</xsl:text>
      <xsl:call-template name="newline"/>
      <xsl:text>*can't estimate expected homozygosity*</xsl:text>
     </xsl:when>
     
     <xsl:otherwise>
      
      <!-- print specified fields then do templates for pvalue -->

      <xsl:text>Observed F: </xsl:text>
      <xsl:value-of select="observed"/>
      <xsl:text>, Expected F: </xsl:text>
      <xsl:value-of select="expected"/>
      <xsl:text>, Normalized deviate (Fnd): </xsl:text>
      <xsl:value-of select="normdev"/>
      <xsl:call-template name="newline"/>
      <xsl:text>p-value range: </xsl:text>

      <!-- treat pvalue differently, since it is not a simple value, but
      has an upper and lower bound -->
      <xsl:apply-templates select="pvalue" mode="bounded"/>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>


 <xsl:template match="homozygosityEWSlatkinExact">
  <xsl:call-template name="section">
   <xsl:with-param name="title">
    <xsl:call-template name="locus-header">
     <xsl:with-param name="title">
      <xsl:text>Slatkin's implementation of EW homozygosity test of neutrality</xsl:text>
     </xsl:with-param>
    </xsl:call-template>
   </xsl:with-param>
   <xsl:with-param name="level" select="3"/>
   <xsl:with-param name="text">

    <xsl:choose>

     <xsl:when test="@role='no-data'">
      <xsl:text>*No data*</xsl:text>
     </xsl:when>
     
     <xsl:otherwise>
      
      <!-- print specified fields invoking the template for  -->

      <xsl:text>Expected F: </xsl:text>
      <xsl:value-of select="meanHomozygosity"/>
      <xsl:text>, Variance in F: </xsl:text>
      <xsl:value-of select="varHomozygosity"/>
      <xsl:text>, p-value of F: </xsl:text>

      <!-- treat pvalue differently, get significance based on a -->
      <!-- two-tailed test -->
      <xsl:call-template name="pvalue-func">
       <xsl:with-param name="val" select="probHomozygosity"/>
       <xsl:with-param name="type" select="'two-tailed'"/>
      </xsl:call-template>

      <!--
      <xsl:call-template name="newline"/>
      <xsl:text>Theta: </xsl:text>
      <xsl:value-of select="theta"/>
      <xsl:text>, p-value for Ewens test: </xsl:text>
      <xsl:call-template name="pvalue-func">
       <xsl:with-param name="val" select="probEwens"/>
      </xsl:call-template>
      -->

     </xsl:otherwise>
    </xsl:choose>
   </xsl:with-param>
  </xsl:call-template>
  
 </xsl:template>
 

 <!-- ################  END HOMOZYGOSITY STATISTICS ###################### --> 

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
 