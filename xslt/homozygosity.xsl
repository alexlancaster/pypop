<!--
This file is part of PyPop

  Copyright (C) 2003. The Regents of the University of California (Regents) 
  All Rights Reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.
-->
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

     <xsl:when test="@role='no-data'">
      <xsl:text>*No data*</xsl:text>
     </xsl:when>

     <xsl:when test="@role='out-of-range'">
      <xsl:text>Observed F: </xsl:text>
      <xsl:value-of select="observed"/>
      <xsl:call-template name="newline"/>
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

     <xsl:when test="@role='monomorphic'">
      <xsl:text>*Monomorphic, exact test cannot be run*</xsl:text>
     </xsl:when>
     
     <xsl:otherwise>
      
      <!-- print specified fields invoking the template for  -->

      <xsl:text>Observed F: </xsl:text>
      <xsl:value-of select="observedHomozygosity"/>
      <xsl:text>, Expected F: </xsl:text>
      <xsl:value-of select="meanHomozygosity"/>
      <xsl:text>, Variance in F: </xsl:text>
      <xsl:value-of select="varHomozygosity"/>
      <xsl:call-template name="newline"/>
      <xsl:text>Normalized deviate of F (Fnd): </xsl:text>
      <xsl:value-of select="normDevHomozygosity"/>
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

 <xsl:template match="homozygosityEWSlatkinExactPairwise">

  <xsl:call-template name="newline"/>

  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar">Locus</xsl:with-param>
   <xsl:with-param name="length" select="15"/>
   <xsl:with-param name="type" select="'left'"/>
  </xsl:call-template>
  
  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar">F_obs</xsl:with-param>
   <xsl:with-param name="length" select="8"/>
   <xsl:with-param name="type" select="'right'"/>
  </xsl:call-template>
  
  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar">F_obs</xsl:with-param>
   <xsl:with-param name="length" select="8"/>
   <xsl:with-param name="type" select="'right'"/>
  </xsl:call-template>
  
  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar">Var(F)</xsl:with-param>
   <xsl:with-param name="length" select="8"/>
   <xsl:with-param name="type" select="'right'"/>
  </xsl:call-template>
  
  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar">F_nd</xsl:with-param>
   <xsl:with-param name="length" select="8"/>
   <xsl:with-param name="type" select="'right'"/>
  </xsl:call-template>
  
  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar"> p-value</xsl:with-param>
   <xsl:with-param name="length" select="8"/>
   <xsl:with-param name="type" select="'left'"/>
  </xsl:call-template>
    
  <xsl:call-template name="newline"/>

  <xsl:for-each select="group">

   <xsl:call-template name="justified-cell">
    <xsl:with-param name="padVar" select="@locus"/>
    <xsl:with-param name="length" select="15"/>
    <xsl:with-param name="type" select="'left'"/>
   </xsl:call-template>

   <xsl:call-template name="justified-cell">
    <xsl:with-param name="padVar" select="homozygosityEWSlatkinExact/observedHomozygosity"/>
    <xsl:with-param name="length" select="8"/>
    <xsl:with-param name="type" select="'right'"/>
   </xsl:call-template>

   <xsl:call-template name="justified-cell">
    <xsl:with-param name="padVar" select="homozygosityEWSlatkinExact/meanHomozygosity"/>
    <xsl:with-param name="length" select="8"/>
    <xsl:with-param name="type" select="'right'"/>
   </xsl:call-template>
   
   <xsl:call-template name="justified-cell">
    <xsl:with-param name="padVar" select="homozygosityEWSlatkinExact/varHomozygosity"/>
    <xsl:with-param name="length" select="8"/>
    <xsl:with-param name="type" select="'right'"/>
   </xsl:call-template>
   
   <xsl:call-template name="justified-cell">
    <xsl:with-param name="padVar" select="homozygosityEWSlatkinExact/normDevHomozygosity"/>
    <xsl:with-param name="length" select="8"/>
    <xsl:with-param name="type" select="'right'"/>
   </xsl:call-template>
   
   <xsl:call-template name="justified-cell">
    <xsl:with-param name="padVar">
     <xsl:text> </xsl:text>
     <xsl:call-template name="pvalue-func">
      <xsl:with-param name="val" select="homozygosityEWSlatkinExact/probHomozygosity"/>
      <xsl:with-param name="type" select="'two-tailed'"/>
     </xsl:call-template>
    </xsl:with-param>
    <xsl:with-param name="length" select="8"/>
    <xsl:with-param name="type" select="'left'"/>
   </xsl:call-template>
  
   
   <xsl:call-template name="newline"/>
  </xsl:for-each>

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
 
